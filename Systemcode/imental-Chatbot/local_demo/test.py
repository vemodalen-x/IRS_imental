import paddlehub as hub
import os

module = hub.Module(name="ernie_gen")
module.export(params_path=r'/root/paddlejob/workspace/train_data/datasets/data113576/medical_cn_qa.params', module_name="ernie_gen_medical", author="vemodalen")
os.system("hub install ernie_gen_medical")
print('export done')
medical_qa = hub.Module(name="ernie_gen_medical")
print('medical_qa load')
