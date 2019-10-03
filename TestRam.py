# -*- coding: utf-8 -*-
import sys
# sys.path.append('C:\\Users\\chengxu01'
#                 '\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib')
#sys.path.append('C:\\Users\\chengxu01'
#                '\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages')
# sys.path.append('C:\\Users\\chengxu01\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\test')
sys.path.append('lib')
sys.path.append('lib\\site-packages\\xlwt-1.3.0-py2.7.egg')
# sys.path.append('lib\\site-packages\\xlrd-1.1.0-py2.7.egg')
# sys.path.append('lib\\site-packages\\xlwt-1.3.0-py2.7.egg')
# import t1
# import subprocess
import os
import xlwt
import time
import re
import datetime


ExcRamName = "TestRam"  # Excel名字
SheetName = "TestRam"  # sheet页名字
RollTime = 5   # 测试时间 默认值150
TimeSpan = 6     # 时间间隔
SaveExcPath = "C:\\"  # 保存路径
ExcName = ""
workbook = ""
worksheet = ""
SaveTempFilePath = "D:"
fg = 0  # fps回调停止标识
thermaltype = 0 #-1未找到对应cpu型号，0还为获取，1高通系列cpu

# 读取结束信息，根据前端的停止标识觉得是否读取数据
def ReadStop():
    '''
    读取结束信息，根据前端的停止标识觉得是否读取数据
    :return: 1停止测试，0继续测试
    '''
    try:
        txtName = SaveTempFilePath + "\\codingWord.txt"
        f = open(txtName, "r")
        stop = f.read()
        # f.closed()
        return stop
    except:
        return '0'
# ram数据获取后写入RamNum.txt，前端读取后可实时显示
def WriteRamNum(Ram):
    '''
    ram数据获取后写入RamNum.txt，前端读取后可实时显示
    :param Ram: 需要记录的Ram值
    :return:
    '''
    try:
        txtName = SaveTempFilePath + "\\RamNum.txt"
        f1 = open(txtName, "w")
        f1.write(str(Ram))
        # f.closed()
        f1.close()
        return
    except:
        return '0'

def UpdateRollTime(num):
    global RollTime
    RollTime = num
# 接收前端传值，修改默认值,进行初始化
def CtoPythonStr(_ExcRamName,_SheetName,_RollTime,_TimeSpan,_SaveExcPath,_SaveTempFilePath):
    '''
    接收前端传值，修改默认值,进行初始化
    :param _ExcRamName: Excel名字,默认值为"TestRam"
    :param _SheetName: sheet页名字，默认值为"TestRam"
    :param _RollTime: 测试时间，循环测试的次数
    :param _TimeSpan: 时间间隔，默认值为6
    :param _SaveExcPath: Excel的保存路径
    :param _SaveTempFilePath: codingWord.txt和RamNum.txt的保存路径
    :return:
    '''
    if not _ExcRamName.strip() == "":
        global ExcRamName
        ExcRamName = _ExcRamName
    if not _SheetName.strip() == "":
        global SheetName
        SheetName = _SheetName
    if not _RollTime.strip() == "":
        global RollTime
        RollTime = _RollTime
    if not _TimeSpan.strip() == "":
        global TimeSpan
        TimeSpan = _TimeSpan
    if not _SaveExcPath.strip() == "":
        global SaveExcPath
        SaveExcPath = _SaveExcPath
    if not _SaveTempFilePath.strip() == "":
        global SaveTempFilePath
        SaveTempFilePath = _SaveTempFilePath
    global ExcName
    ExcName = ExcRamName + "_" + str(time.strftime("%H_%M_%S_")) + str(time.time()) + ".xls"
# 定义sheet页名称
    global workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    global worksheet
    worksheet = workbook.add_sheet(SheetName)
# 初始化列名
    worksheet.write(0, 0, '时间')
    worksheet.write(0, 1, '应用占用内存Native(KB)')
    worksheet.write(0, 2, '应用占用内存Dalvik(KB)')
    worksheet.write(0, 3, '应用占用内存TotalPss(MB)')
    worksheet.write(0, 4, '类windows应用占用CPU率(%)')
    worksheet.write(0, 5, '类Emmagee应用占用CPU率(%)')
    worksheet.write(0, 6, '电量(%)')
    worksheet.write(0, 7, 'fps')
    worksheet.write(0, 8, 'Draw call')
    worksheet.write(0, 9, 'cpu温度(℃)*测试中')
    a = GetNum()
    print(a)
    return a
# 按sp内容进行数据格式化，例传入"："，按:进行格式化数据
def listcle(s, sp=" "):  # 将这一行，按空格分割成一个list,
    '''
    按sp内容进行数据格式化，例传入"："，按:进行格式化数据
    :param s: 待格式化的str
    :param sp: 格式化所需的标识
    :return:
    '''
    li = s.split(sp)
    while '' in li:  # 将list中的空元素删除
        li.remove('')
    return li
# 保存Excel
def SaveExcel():
    global SaveExcPath
    SaveExcPathName = SaveExcPath + ExcName
    workbook.save(SaveExcPathName)
# 获取内存，返回一个数组
def Select_Ram():
    '''
    获取内存，返回一个数组
    :return: NativeHeap, DalvikHeap, TotalPss
    '''
    Nc_lines = os.popen("D:\\adb shell dumpsys meminfo cn.jj ").readlines()  # 逐行读取

    for line in Nc_lines:
        l = listcle(line, " ")
        if l[0] == "Native" and l[1] == "Heap":
            NativeHeap = l[7]
        if l[0] == "Dalvik" and l[1] == "Heap":
            DalvikHeap = l[7]
        if l[0] == "TOTAL":
            TotalPss = l[1]
    return NativeHeap, DalvikHeap, TotalPss
# 获取电量，并且取到对应的
def Select_DL():
    '''
    获取电量，并且取到对应的
    :return:DL
    '''
    Dl_lines = os.popen("D:\\adb shell dumpsys battery ").readlines()
    for levl in range(0, len(Dl_lines)):
        if 'level' in Dl_lines[levl]:
            DL = listcle(Dl_lines[levl], ":")[1]
            return DL

def Select_Like_Windows_CPU():

    ss = []
    # W_Cpu_lines = subprocess.Popen('D:\\adb shell top -n 1 -d 1 | findstr cn.jj', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # W_Cpu_lines = os.popen("D:\\adb shell top -n 1 -d 1 | findstr cn.jj").readlines()
    # while W_Cpu_lines.poll() is None:
    #     line = W_Cpu_lines.stdout.readline()
    #     # for n in range(0, len(line)):
    #     ss.append(listcle(str(line), " "))
    #     for c1 in range(0, len(ss)):
    #         if listcle(ss[c1][len(ss[c1])-1], "\\")[0] == "cn.jj":
    #             W_Cpu = ss[c1][2]
    #             return W_Cpu
    # W_Cpu_lines = os.popen("D:\\adb devices").readlines()
    W_Cpu_lines = os.popen("D:\\adb shell top -n 1 -d 1").readlines()
    W_Cpu_lines = [x.strip() for x in W_Cpu_lines]  # 处理\n
    W_Cpu_lines = [x.strip() for x in W_Cpu_lines if x.strip() != '']  # 处理空格
    for n in range(0, len(W_Cpu_lines)):
        ss.append(listcle(W_Cpu_lines[n], " "))
        if ss[0][len(ss[0])-1] == "cn.jj":
            return ss[0][2]  # 找到cn.jj后返回CPU值
        else:
            ss = []
            continue
    # for c1 in range(0, len(ss)):
    #     #for c2 in range(0, len(ss[c1])):
    #     if re.sub('[\r\n]', '', ss[c1][len(ss[c1])-1]) == "cn.jj":
    #         W_Cpu = ss[c1][2]
    #         return W_Cpu
    return 0

def Select_Like_Emm_CPU():
    ss = []
    E_Cpu_lines = os.popen("D:\\adb shell dumpsys cpuinfo cn.jj ").readlines()
    for n in range(0, len(E_Cpu_lines)):
        ss.append(listcle(E_Cpu_lines[n], " "))
    for c1 in range(0, len(ss)):
        for c2 in range(0, len(ss[c1])):
            if "cn.jj" in re.sub('[\r\n\t]', '', ss[c1][c2]):
                E_Cpu = ss[c1][2]
                return E_Cpu
    return 0
# 读取jjlog_fps.log中fps和drawcall数据
def Select_fpsORdrawCall():
    global fg
    while fg < 4:
        # fps_lines = "/system/bin/sh: cat: jjlog_fps.log: No such file or directory"未找到的错误信息
        fps_lines = os.popen("D:\\adb shell cat /sdcard/jjlog_fps.log ").readlines()  # 逐行读取
        if "No such file or directory" in fps_lines[0] or fg == 3:
            fps = 100000
            drawcall = 100000
            fg = 0
            break
        else:
            if fps_lines:
                fpsORdrawcall = listcle(fps_lines[0], " ")
                fps = fpsORdrawcall[2]
                drawcall = fpsORdrawcall[6]
                fg = 0
                break
            else:
                fg += 1
                continue
    return fps, drawcall
#获取数据
def GetCpuModel():
    global thermaltype
    CM = os.popen("D:\\adb shell cat /sys/class/thermal/thermal_zone7/type").readlines()
    if "tsens_tz" in CM[0]:
        thermaltype = 1
    else:
        thermaltype = -1
    return
def Select_CpuTemperature():
    if thermaltype != 0:
        if thermaltype == 1:
            CT = os.popen("D:\\adb shell cat /sys/class/thermal/thermal_zone0/temp").readlines()
            CT = CT[0]
            return CT
        else:
            CT = 0
            return CT
    else:
        GetCpuModel()
        C = Select_CpuTemperature()
        return C
def GetNum():

    for num in range(1, int(RollTime)+1):
        # 获取内存
        RamList = Select_Ram()
        # 获取电量，并且取到对应的
        DLNum = Select_DL()
        # 类windows应用占用CPU率(%)
        W_Cpu = Select_Like_Windows_CPU()
        # 类Emmagee应用占用CPU率(%)
        E_Cpu = Select_Like_Emm_CPU()
        # 获取fps,drawcall
        fps, drawcall = Select_fpsORdrawCall()
        #获取cpu温度
        CT = Select_CpuTemperature()
        # 写入excel:NativeHeap,DalvikHeap,应用占用内存Na+Da,应用占用CPU率(%)电量(%)
        worksheet.write(num, 0, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(num, 1, int(RamList[0]))  # NativeHeap
        worksheet.write(num, 2, int(RamList[1]))  # DalvikHeap
        worksheet.write(num, 3, round(int(RamList[2]) / 1024, 2))  # TotalPss
        worksheet.write(num, 4, W_Cpu)
        worksheet.write(num, 5, E_Cpu)
        worksheet.write(num, 6, int(DLNum))  # 电量(%)
        worksheet.write(num, 7, float(fps))
        worksheet.write(num, 8, int(drawcall))
        worksheet.write(num, 9, float(int(CT)/1000))# cpu温度(℃)

        WriteRamNum(int(RamList[2]))# 将内存值写入txt

        t = ReadStop().strip('\n')
        if num == int(RollTime)or t == '1':
            SaveExcel()
            break
        else:
            time.sleep(int(TimeSpan)-2)
    return "0"


if __name__ == '__main__':
    CtoPythonStr("test1", "test1", "10000000", "3", "E:\\", "D:\\")