# -*- encoding=utf8 -*-
__author__ = "xuelin"

from airtest.core.api import *

auto_setup(__file__)
import sys 
sys.path.append('D:\Python35\Lib\site-packages')
sys.path.append('F:\AirtestCaseCollection\Autoxingneng.air')
from multiprocessing import Process
from TestRam import CtoPythonStr

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:旧字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
p = Process(target=CtoPythonStr,args=('test1','test1','10000000','3','E:\\','D:\\')) # 创建一个子进程
alter("D:\\codingWord.txt", "1", "0") # 每次执行前修改固定文件值
p.start()
# 示例Airtest脚本DEMO
for i in range(1, 5):
    touch(Template(r"tpl1558577140764.png", record_pos=(0.381, 0.8), resolution=(1080, 1920)))
    sleep(3)
    touch(Template(r"tpl1558578901653.png", record_pos=(0.382, 0.798), resolution=(1080, 1920)))
    sleep(3)
alter("D:\\codingWord.txt", "0", "1") # 修改文件值，停止采集性能数据

