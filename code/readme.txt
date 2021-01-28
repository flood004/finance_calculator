这是我自己做的记账用的软件，可能有很多不足，但我从命令提示符改成窗口后感觉成就感还是不错的
这是第三版，
如果后续再修改，请使用以下打包方法：

D:
CD D:\Apython\account_calculator_v3
pyinstaller --clean --win-private-assemblies -F -w D:\Apython\account_calculator_v3\main.py

然后可以再D:\Apython\account_calculator_v3\dist里找到exe 文件

如果需要调试
pyinstaller --clean --win-private-assemblies -D D:\Apython\account_calculator_v3\main.py
这个命令是生产文件夹的命令

如果电脑还没按照pyinstaller，以下命令安装，如果还没装python ，我就不写了


python pyinstaller.py -F -w myfile.py 