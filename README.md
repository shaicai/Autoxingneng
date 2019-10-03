Airtest性能自动化
一．现有成果
已实现在执行Airtest脚本的同时，采集游戏当前的性能数据。
例如场景一，现有游戏Airtest脚本，需要测试游戏的性能，即游戏脚本同时，游戏性能数据就可直接获取，摆脱了之前需要手动操作的困扰，在需要长时间运行游戏判断游戏的性能是否正常的场景下，能让测试人员节约大量的时间。
二．使用注意
1.使用本机的cmd运行，暂不支持其他方式运行。
2.安装Python环境，安装Python插件Airtest及xlwt，相关命令为pip install Airtset和pip install xlwt
3.向D盘拷入adb文件（共3个，为了支持性能采集脚本），adb.exe，AdbWinUsbApi.dll及AdbWinApi.dll，可以到Python的airtest插件下粘贴。
4.在文件Autoxingneng.py中修改两个依赖路径，路径1为本地的python插件包路径，示例：sys.path.append('D:\Python35\Lib\site-packages')，路径2为存放Airtest脚本的路径，示例：sys.path.append('F:\AirtestCaseCollection\Autoxingneng.air')。
5.修改性能数据excel的输入位置，确保设置的位置和运行的计算机相符，具体为target=CtoPythonStr,args=('test1','test1','10000000','3','E:\\','D:\\')，。