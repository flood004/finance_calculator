# -*- coding: UTF-8 -*-
import re,datetime,os
from pandas import tseries

#加载文件函数b

dict_in={}#定义空的字典用来存放数据
record_dict={}
records={}
queryrd={}
display={}
dict_order={}
#分隔函数，吧传入的每一行数据进行处理并存入字典
def getstr(str_1): #定义函数1读取文件后按','号分隔为多行数据
	list_str1=str_1.split(',')#按','号分隔为多行数据2
	line_str=[]
	for i in list_str1:
		x=re.sub(r'[\n{}\']','',i).lstrip()#剔除记录中的换行符,用正则去掉特殊字符并去除前后空格
		line_str.append(x) 
	line_tup=line_str # 把list转换为元组？ 
	tuple(line_tup)
	
	for item in line_tup:
		dict={item.split(':')[0]:float(item.split(':')[1])} #循环取出每个key，value对，定义单个字典并更新到开头定义的空字典中{item.split(':')[0]:flot(item.split(':')[1])}
		dict_in.update(dict)
		
def getstrnan(str_1): #定义函数1读取文件后按','号分隔为多行数据
	list_str1=str_1.split(',')#按','号分隔为多行数据
	line_str=[]
	for i in list_str1:
		x=re.sub(r'[\n{}\']','',i).lstrip()#剔除记录中的换行符,用正则去掉空格，{，}等字符
		line_str.append(x) 
	line_tup=line_str # 把list转换为元组，为什么呢？ 
	tuple(line_tup)
	
	for item in line_tup:
		dict={item.split(':')[0]:item.split(':')[1]} #{item.split(':')[0]:flot(item.split(':')[1])}
		dict_in.update(dict)

#读取函数，读取文件的每一行并调用分隔函数
def list_dict(file_1):
    file = open(file_1, "r+",encoding='UTF-8')
    while True:
        line = file.readline()
        if line:
            getstr(line)
        if not line:
            break
    file.close()
#检查文件是否存在，是否为空
if os.path.exists("dict.txt"):#D:\\python_dict\\ 为了防止错误不用绝对路径了
        if os.path.getsize("dict.txt"):
                print('exist and not null')
        else:
                print('exist and null')
else:
        print('file not exist')
        



#查询统计函数，对字典内所有 小于等于输入日期的值就和
def total_takings(yearly_record,endt):
        nsum = 0.0000
        
        for i in yearly_record:
                s = datetime.datetime.strptime(i,'%Y-%m-%d %H/%M/%S')
                if s <= endt:
                        nsum =nsum+ yearly_record[i]
                else:
                        nsum =nsum
        return nsum
		
#删除函数，单条删除记录
def del_records (rname,ddate):
    del rname[ddate]

#删除函数，批量删除记录
def del_recordsp (rname,stdate,etdate):
        sdate=datetime.datetime.strptime(stdate+' 00/00/00','%Y-%m-%d %H/%M/%S')
        edate=datetime.datetime.strptime(endate+' 23/59/59','%Y-%m-%d %H/%M/%S')
        for v in dname:
                ddate=datetime.datetime.strptime(v,'%Y-%m-%d %H/%M/%S')
                if ddate >=sdate and ddate<=edate:
                        del rname[v]
        print('删除完毕')

	
#查询函数，查询时间段内的所有记录

def query_records(dname,stdate,endate=datetime.datetime.now().strftime('%Y-%m-%d')):

        sdate=datetime.datetime.strptime(stdate+' 00/00/00','%Y-%m-%d %H/%M/%S')
        edate=datetime.datetime.strptime(endate+' 23/59/59','%Y-%m-%d %H/%M/%S')
    
        for v in dname:
                ddate=datetime.datetime.strptime(v,'%Y-%m-%d %H/%M/%S')
                if ddate >=sdate and ddate<=edate:
                        display[v]=dname[v]
        print(display)
        display.clear()




#新增修改函数，插入和修改当前记录
def recordin (opcode):
        if (opcode == 1):
                print ('input code is :',opcode)
                transactioncode=input('请输入类型代码 I 为收入 C 为支出:\n>>>>')
                if (transactioncode=='i' or transactioncode=='I'):
                        #print ('收入类型' )
                        abscode=1
                if (transactioncode=='c' or transactioncode=='C'):
                        
                        #print ('支出类型')
                        abscode=-1
                        
                idatestr=input('请输入日期 (格式为2019-06-01) 输入0默认当前时间:\n>>>>')
                if (idatestr=='0'):
                        idate=datetime.datetime.now()#time.localtime() 用daeime更直观一些
                else:
                        idate=datetime.datetime.strptime(idatestr,'%Y-%m-%d') #time.strptime(idatestr,'%Y-%m-%d')


                outdate=idate.strftime('%Y-%m-%d %H/%M/%S')#time.strftime('%Y-%m-%d %H/%M/%S',idate)
                #print (outdate)

                inputn=int(input('请输入持续月份:\n>>>>'))
                
                amountstr=input('请输入金额:\n>>>>')
                amount=float(amountstr)
                
                i=inputn-1
                while i>=0 :
                        datex=datetime.datetime.strptime(outdate, "%Y-%m-%d %H/%M/%S")
                        datei=datex + tseries.offsets.DateOffset(months=i)#relativedelta(months=1) # relativedelta(years=1) datetime.timedelta(months = 1)
                        outdatei=datei.strftime('%Y-%m-%d %H/%M/%S')
                        if outdatei in record_dict:
                                print('====================================\n已有记录，进行更新：')
                                #print(record_dict)
                        else:
                                print ('====================================\n新记录')
                                #print(record_dict)
                        record_dict[outdatei]=abscode*amount
                        i=i-1
                        
                #datelist=datetime.strptime(outdate, "%Y-%m-%d-%H")
                
                print (record_dict)
                f = open('dict.txt','w')
                f.writelines(str(record_dict))
                f.close()
                        
        elif (opcode == 2):
                transactioncode=input('请输入类型代码 I 为收入 C 为支出:\n>>>>')
                
                if (transactioncode=='i' or transactioncode=='I'):
                        abscode=1
                if (transactioncode=='c' or transactioncode=='C'):
                        abscode=-1
                idatestr=input('请输入日期 (格式为2019-06-01 13/32/01) 输入0默认当前时间:\n>>>>')
                if (idatestr=='0'):
                        idate=datetime.datetime.now()
                else:
                        idate=datetime.datetime.strptime(idatestr,'%Y-%m-%d %H/%M/%S') #idate=time.strptime(idatestr,'%Y-%m-%d %H/%M/%S')


                outdate=idate.strftime('%Y-%m-%d %H/%M/%S')#time.strftime('%Y-%m-%d %H/%M/%S',idate)
                #print (outdate)

                amountstr=input('请输入金额:')
                amount=float(amountstr)
                
                if outdate in records:
                        print('====================================\n已有记录，进行更新')
                        records[outdate]=abscode*amount
                        #print (records.items())
                else:
                        print ('====================================\n新记录')
                        records[outdate]=abscode*amount
                        #print (records.items())
                        
                f = open('records.txt','w')
                f.writelines(str(records))
                f.close()

        elif (opcode == 3):
                
                #print ('input code is :',opcode)
                idatestr=input('请输入日期 (格式为2019-06-01):')
                idate=datetime.datetime.strptime(idatestr,'%Y-%m-%d')#time.strptime(idatestr,'%Y-%m-%d')
                outdate=idate.strftime('%Y-%m-%d')#time.strftime('%Y-%m-%d',idate)
                #print(outdate)
                queryrd.update(record_dict)
                queryrd.update(records)
                outn=total_takings(queryrd,idate)
                print(outn)
                queryrd.clear()
                



		
#操作区分函数
def optype(ocode=0):
    if ocode==3:
            recordin(ocode)#查询可用额直接调
    elif ocode==0:
            print('exit')
    else:
            op=int(input('请输入操作类型:\n1:查询\n2:增改\n3:删除\n0:退出 \n>>>>'))
            if op==1:
                    startt=input('请输入开始日期 (格式为2019-01-01) :\n>>>>')
                    endt=input('请输入截止日期 (格式为2019-12-01) 默认截止到该日期23:59:59,输入0默认当前日期:\n>>>>')
                    if endt=='0':
                            endtt=datetime.datetime.now().strftime('%Y-%m-%d')
                    else:
                            endtt=endt
                    #根据选择的类型选择不同的字典
                    if ocode==1:
                            query_records(record_dict,startt,endtt)
                    if ocode==2:
                            query_records(records,startt,endtt)
            if op==2:
                    #如果增改则直接调用增改函数
                    recordin(ocode)
            if op==3:
                    #调删除函数
                    dstart=input('请输入要删除记录的开始日期 (格式为2019-01-01)默认00:00:00开始 :\n>>>>')
                    dendt=input('请输入要删除记录的截止日期 (格式为2019-12-01) 默认截止到该日期23:59:59,输入0默认当前日期:\n>>>>')
                    if dendt=='0':
                            ddendt=datetime.datetime.now().strftime('%Y-%m-%d')
                    else:
                            ddendt=dendt
                    if ocode==1:
                            del_recordsp(record_dict,startt,endtt)
                    if ocode==2:
                            del_recordsp(records,startt,endtt)

	
opcodetype=int(input('欢迎使用财务统计功能！可以把固定的收入支出登记，保持记录明细后可自动计算可支配余额！\n==============================\n请选择操作类型,\n  1:固定收入支出; 2:非固定收入支出 ;3:查询特定日期的可用支出金额:\n>>>'))
#调用函数导入文件到字典里
list_dict("dict.txt")

dict_order=sorted(dict_in.items(),key=lambda x:x[0])
record_dict.update(dict_order)#开始用=但是当dict_in 被清空的时候也一块被清空了。。
#print("dict read from local : ", record_dict)

dict_in.clear()#两次调用之间清空存放数据的字典，
dict_order.clear()
list_dict("records.txt")
dict_order=sorted(dict_in.items(),key=lambda x:x[0])
records.update(dict_order)
#print("detail read from local : ", records)
#调用主函数
optype(opcodetype)
opcodetypeloop=int(input('==============================\n是否还有其它操作？\n  0：退出;\n  1:固定收入支出;\n  2:非固定收入支出;\n  3:查询特定日期的可用支出金额;\n >>>'))

while opcodetypeloop>0:
        
        optype(opcodetypeloop)
        opcodetypeloop=int(input('==============================\n是否还有其它操作？\n  0：退出;\n  1:固定收入支出;\n  2:非固定收入支出;\n  3:查询特定日期的可用支出金额:\n >>>'))

print('感谢使用财务统计功能!!')





                
