import paddlenlp
from paddlenlp.transformers import SkepForSequenceClassification, SkepTokenizer
import os
import paddle
from functools import partial

import numpy as np
import paddle.nn.functional as F
from paddlenlp.data import Stack, Tuple, Pad



def convert_example(example,
                    tokenizer,
                    max_seq_length=512,
                    is_test=False):
    encoded_inputs = tokenizer(
        text=example["text"], max_seq_len=max_seq_length)


    input_ids = encoded_inputs["input_ids"]
    # token_type_ids
    token_type_ids = encoded_inputs["token_type_ids"]

    if not is_test:
        # label
        label = np.array([example["label"]], dtype="int64")
        return input_ids, token_type_ids, label
    else:
        # qid = np.array([example["qid"]], dtype="int64")
        return input_ids, token_type_ids

def create_dataloader(dataset,
                      trans_fn=None,
                      mode='train',
                      batch_size=1,
                      batchify_fn=None):
    if trans_fn:
        dataset = dataset.map(trans_fn)

    shuffle = True if mode == 'train' else False
    if mode == "train":
        sampler = paddle.io.DistributedBatchSampler(
            dataset=dataset, batch_size=batch_size, shuffle=shuffle)
    else:
        sampler = paddle.io.BatchSampler(
            dataset=dataset, batch_size=batch_size, shuffle=shuffle)
    dataloader = paddle.io.DataLoader(
        dataset, batch_sampler=sampler, collate_fn=batchify_fn)
    return dataloader
def predict(model, data, tokenizer, label_map, batch_size=1):
    """
    Predicts the data labels.

    Args:
        model (obj:`paddle.nn.Layer`): A model to classify texts.
        data (obj:`List(Example)`): The processed data whose each element is a Example (numedtuple) object.
            A Example object contains `text`(word_ids) and `se_len`(sequence length).
        tokenizer(obj:`PretrainedTokenizer`): This tokenizer inherits from :class:`~paddlenlp.transformers.PretrainedTokenizer` 
            which contains most of the methods. Users should refer to the superclass for more information regarding methods.
        label_map(obj:`dict`): The label id (key) to label str (value) map.
        batch_size(obj:`int`, defaults to 1): The number of batch.

    Returns:
        results(obj:`dict`): All the predictions labels.
    """
    examples = []
    for text in data:
        input_ids, segment_ids = convert_example(
            text,
            tokenizer,
            max_seq_length=128,
            is_test=True)
        examples.append((input_ids, segment_ids))

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # input id
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # segment id
    ): fn(samples)

    # Seperates data into some batches.
    batches = []
    one_batch = []
    for example in examples:
        one_batch.append(example)
        if len(one_batch) == batch_size:
            batches.append(one_batch)
            one_batch = []
    if one_batch:
        # The last batch whose size is less than the config batch_size setting.
        batches.append(one_batch)

    results = []
    model.eval()
    for batch in batches:
        input_ids, segment_ids = batchify_fn(batch)
        input_ids = paddle.to_tensor(input_ids)
        segment_ids = paddle.to_tensor(segment_ids)
        logits = model(input_ids, segment_ids)
        probs = F.softmax(logits, axis=1)
        idx = paddle.argmax(probs, axis=1).numpy()
        idx = idx.tolist()
        labels = [label_map[i] for i in idx]
        results.extend(labels)
    return results

    
if __name__ == '__main__':
    MODEL_NAME = "ernie-1.0"

    model = SkepForSequenceClassification.from_pretrained(pretrained_model_name_or_path="skep_ernie_1.0_large_ch", num_classes=19)
    tokenizer = SkepTokenizer.from_pretrained(pretrained_model_name_or_path="skep_ernie_1.0_large_ch")

    batch_size=1
    params_path = 'pretrained_model\model_state.pdparams'

    if params_path and os.path.isfile(params_path):
        # load
        state_dict = paddle.load(params_path)
        model.set_dict(state_dict)
        print("Loaded parameters from %s" % params_path)

    print('init done')

    data = [
        {"text":'我担心和同学同事的关系，无所适从','qid':''},
        {"text":'我挺开心的没事 哈哈哈啊哈','qid':''},
        {"text":'我女朋友对我太坏了，我被那个坏女人伤透了心','qid':''},
        {"text":'太难了学不下去了','qid':''},
        {"text":'哎我晚上一直睡不着怎么办呀','qid':''},
    ]

    results = predict(
        model, data, tokenizer, label_map, batch_size=batch_size)
    for idx, text in enumerate(data):
        print('Data: {} \t Label: {}'.format(text, results[idx]))
