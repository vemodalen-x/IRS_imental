######  欢迎使用脚本任务，首先让我们熟悉脚本任务的一些使用规则  ######
# 详细教程请在AI Studio文档(https://ai.baidu.com/ai-doc/AISTUDIO/Ik3e3g4lt)中进行查看.
# 脚本任务使用流程：
# 1.编写代码/上传本地代码文件
# 2.调整数据集路径以及输出文件路径
# 3.填写启动命令和备注
# 4.提交任务选择运行方式(单机单卡/单机四卡/双机四卡)
# 5.项目详情页查看任务进度及日志
# 注意事项：
# 1.输出结果的体积上限为20GB，超过上限可能导致下载输出失败.
# 2.脚本任务单次任务最大运行时长为72小时（三天）.
# 3.在使用单机四卡或双击四卡时可不配置GPU编号，默认启动所有可见卡；如需配置GPU编号，单机四卡的GPU编号为0,1,2,3；双机四卡的GPU编号为0,1.
# 日志记录. 任务会自动记录环境初始化日志、任务执行日志、错误日志、执行脚本中所有标准输出和标准出错流(例如print()),用户可以在「提交」任务后,通过「查看日志」追踪日志信息.
# -------------------------------关于数据集和输出文件的路径问题---------------------------------
# 数据集路径
# datasets_prefix为数据集的根路径，完整的数据集文件路径是由根路径和相对路径拼接组成的。
# 相对路径获取方式：请在编辑项目状态下通过点击左侧导航「数据集」中文件右侧的【复制】按钮获取.
# datasets_prefix = '/root/paddlejob/workspace/train_data/datasets/'
# train_datasets =  datasets_prefix + '通过路径拷贝获取真实数据集文件路径'
# 输出文件路径
# 任务完成后平台会自动把output_dir目录所有文件压缩为tar.gz包，用户可以通过「下载输出」将输出结果下载到本地.
# output_dir = "/root/paddlejob/workspace/output/"
# -------------------------------关于启动命令需要注意的问题------------------------------------
# 脚本任务支持两种运行方式
# 1.shell 脚本. 在 run.sh 中编写项目运行时所需的命令，并在启动命令框中填写如 bash run.sh 的命令使脚本任务正常运行.
# 2.python 指令. 在 run.py 编写运行所需的代码，并在启动命令框中填写如 python run.py <参数1> <参数2> 的命令使脚本任务正常运行.
# 注：run.sh、run.py 可使用自己的文件替代，如python train.py 、bash train.sh.
# 命令示例：
# 1. python 指令
# ---------------------------------------单机四卡-------------------------------------------
# 方式一（不配置GPU编号）：python -m paddle.distributed.launch run.py
# 方式二（配置GPU编号）：python -m paddle.distributed.launch --gpus="0,1,2,3" run.py
# ---------------------------------------双机四卡-------------------------------------------
# 方式一（不配置GPU编号）：python -m paddle.distributed.launch run.py
# 方式二（配置GPU编号）：python -m paddle.distributed.launch --gpus="0,1" run.py
# 2. shell 命令
# 使用run.sh或自行创建新的shell文件并在对应的文件中写下需要执行的命令(需要运行多条命令建议使用shell命令的方式)。
# 以单机四卡不配置GPU编号为例，将单机四卡方式一的指令复制在run.sh中，并在启动命令出写出bash run.sh
wget -P /root/.paddlenlp/models/ernie-1.0   https://paddlenlp.bj.bcebos.com/models/transformers/ernie/ernie_v1_chn_base.pdparams
pip install --upgrade pip
pip install wechaty
pip install paddle-ernie
pip install --upgrade paddlenlp
pip install xlrd
pip install --upgrade paddlehub

# 设置环境变量
export WECHATY_PUPPET=wechaty-puppet-service
export WECHATY_PUPPET_SERVICE_TOKEN="808080"
export WECHATY_PUPPET_SERVICE_ENDPOINT="47.241.77.80:8080" #这里填Wechaty服务端的IP和端口

# 运行python文件
python -m paddle.distributed.launch run.py