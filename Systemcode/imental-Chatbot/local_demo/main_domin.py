# -*- coding: utf-8 -*-

import os
os.environ['WECHATY_PUPPET']="wechaty-puppet-service"
os.environ['WECHATY_PUPPET_SERVICE_TOKEN']="puppet_padlocal_d0b6da8a8ce04e10bb254cbcadf80a31" # Wechaty token
os.environ['CUDA_VISIBLE_DEVICES']="0"
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']="47.241.77.80:8080" #Wechaty ip and port

# os.system("pip install --upgrade pip")
# os.system("pip install pandas")
# os.system("pip install numpy")
# os.system("pip install paddlepaddle-gpu == 2.1.2")
# os.system("pip install paddlenlp")
# os.system("pip install paddle-ernie")
# os.system("pip install xlrd")
# os.system("pip install paddlehub")
# os.system("pip install wechaty")

import re
import argparse
from utils import set_seed, select_response
from collections import deque
import paddlenlp
import paddle
import asyncio
import numpy as np
import paddlehub as hub
from baidu_translate import translate2auto
from plato import PlatoNlp
from paddlenlp import Taskflow
from paddlenlp.transformers import UnifiedTransformerLMHeadModel,UnifiedTransformerTokenizer
from paddlenlp.transformers import SkepForSequenceClassification, SkepTokenizer
from efaqa_emotion import predict

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

module = hub.Module(name="ernie_gen")
module.export(params_path=r'./medical_cn_qa.params', module_name="ernie_gen_medical", author="vemodalen")
os.system("hub install ernie_gen_medical")
print('export success')

print('start loading')
# medical_qa chatbot
# medical_qa = hub.Module(directory=r"/root/paddlejob/workspace/code/ernie_gen_medical/")
medical_qa = hub.Module(name="ernie_gen_medical")
print('medical_qa load')

#daily chatbot
model_tmp='plato-mini'
max_turn=10
PlatoNlpR = PlatoNlp(max_turn=10,model=model_tmp)
print('daily chatbot load')

#emotion chatbot
senta = Taskflow("sentiment_analysis")
print('emotion load')

#efaqa chatbot
model = SkepForSequenceClassification.from_pretrained(pretrained_model_name_or_path="skep_ernie_1.0_large_ch", num_classes=19)
tokenizer = SkepTokenizer.from_pretrained(pretrained_model_name_or_path="skep_ernie_1.0_large_ch")
batch_size=1
params_path = './model_state.pdparams'
if params_path and os.path.isfile(params_path):
    # load
    state_dict = paddle.load(params_path)
    model.set_dict(state_dict)
    print("Loaded parameters from %s" % params_path)
    
label_map = {'?????????': 0, '??????': 1, '??????': 2, '??????????????????': 3, '???????????????': 4, '??????': 5, '????????????': 6, '?????????????????????': 7, '?????????': 8, '????????????': 9, '?????????????????????': 10,
 '???????????????????????????????????????': 11, '??????': 12, '??????': 13, '????????????': 14, '??????': 15, '?????????': 16, 'LGBT': 17, '????????????': 18, '????????????S2': 19, '?????????': 20, 
 '?????????': 21, '????????????': 22, '?????????': 23, '?????????????????????': 24, '?????????': 25, '?????????????????????': 26, '?????????????????????': 27, '??????????????????????????????': 28, '??????': 29, '?????????????????????': 30, '?????????????????????': 31}
label_map = {value:key for key,value in label_map.items()}

print('label_map load')
print('init done')


async def on_message(msg: Message):
    msg_src = msg.text()
    if msg_src == "[NEXT]":
        PlatoNlpR.history.clear()
        await msg.say('I am better now~ hi! I am imental')

    if(msg_src =='hi' or msg_src == '??????'):
        await msg.say('hi! I am imental~ your personel Psychological Consultant??? You can tell me anything you like and I am listening! try start with Q OR D OR M OR E to explore more')

    if len(msg_src) > 0:
        if(len(PlatoNlpR.history)>=max_turn):
            await msg.say("sorry I have no battery???please print '[NEXT]' to start again")
        
        if msg_src.startswith('Q'): #only trigger Q: question
            text_question=msg_src[1:]
            lan, ch_txt = translate2auto(text_question,'auto','zh')
            ch_txt=[ch_txt]
            #since the model is trained by chinese dataset so auto2zh
            results = medical_qa.generate(texts=ch_txt, use_gpu=True, beam_width=1)
            #check input 
            ans = results[0][0]
            if(lan=="zh"):
                ans = ans
            else:
                _,ans = translate2auto(ans,'zh',lan)
            await msg.say('[imental medical Q&A]' + "  " + ans)

        elif  msg_src.startswith('D'):#only trigger D daily talk
            text_question=msg_src[1:]
            try:
                lan, ch_txt = translate2auto(text_question,'auto','zh')
                ch_txt=str(ch_txt)
                ans = PlatoNlpR.predict(ch_txt)
                if(lan=="zh"):
                    ans = ans
                else:
                    _,ans = translate2auto(ans,'zh',lan)
                await msg.say('[imental]' + "  " + ans)
            except:
                await msg.say('sorry I do not understand. please try again or use another language like:chinese or English')

        elif  msg_src.startswith('E'): #only trigger Emotion
            text_question=msg_src[1:]
            lan, ch_txt = translate2auto(text_question,'auto','zh')
            ch_txt=str(ch_txt)
            ans=senta(ch_txt)[0]['label']
            if(ans=="positive"):
                ans="???????????????????????? ??????????????????"
            else :
                ans="???????????????????????? ?????????????????????????????? ????????????????????? ?????????????????????"
            if(lan=="zh"):
                ans = ans
            else:
                _,ans = translate2auto(ans,'zh',lan)
            await msg.say('[imental emotion]' + "  " + ans)
        
        elif  msg_src.startswith('M'): #only trigger Mental Health
            text_question=msg_src[1:]
            lan, ch_txt = translate2auto(text_question,'auto','zh')
            print(ch_txt)
            data=[{'text':str(ch_txt),'qid':''}]
            
            results = predict(model, data, tokenizer, label_map, batch_size=batch_size)
            
            ans=str(results[0])
            if(ans=="??????"):
                ans="????????????????????? ????????? ???????????????"
            else:
                ans="?????????????????????"+ans+"?????????"
            if(lan=="zh"):
                ans = ans
            else:
                _,ans = translate2auto(ans,'zh',lan)
            
            await msg.say('[imental Mental Health]' + "  " + ans+"https://zh.wikihow.com/wikiHowTo?search="+str(results[0]))
        




async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    # print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)
    pass


async def on_login(user: Contact):
    # print(user)
    pass


async def main():
    # make sure we set WECHATY_PUPPET_SERVICE_TOKEN
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Imental Bot started.')


asyncio.run(main())