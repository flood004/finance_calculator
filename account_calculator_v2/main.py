from datetime import datetime
#from db_helper import query,update,insert,delete
import re,os
from db_helper import insert,update,delete,query,initialize,table_check
import log_helper

mname='C:\\Users\\henry.zhangtj\\AppData\\Local\\Programs\\Python\\Python37\\b\\accounting.db'

def queryrecord (opcode,tcode,qiu,dname):
	idatestr=input('请输入日期 (格式为2019-06-01 00:00:00) ,当前时间请输入d ,不输入时间默认为0点:')
	if idatestr.upper()=='D':
		idate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	elif idatestr.upper()=='Y':
		a=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		idate=a.replace(year=a.year, month=1, day=1)
	else:
		it=bool(re.search('\d{1,2}:\d{1,2}:\d{1,2}&',idatestr))

		if it==False:
			idate=datetime.strptime(idatestr,'%Y-%m-%d').strftime('%Y-%m-%d')+' 00:00:00'#time.strptime(idatestr,'%Y-%m-%d')
		else:
			idate=datetime.strptime(idatestr,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

	if opcode==0:
		endate =None
	else:
		if (qiu=='Q' or qiu=='D'):
			endt=input('请输入截止日期 (格式为2019-12-01默认截止到该日期23:59:59) ,输入d当前日期,查询可用请按0跳过:\n>>>>')
			if endt=='d':
				endate=datetime.now().strftime('%Y-%m-%d')+' 23:59:59'
			elif endt=='0':
				endate =None
			else:
				endate=datetime.strptime(endt,'%Y-%m-%d').strftime('%Y-%m-%d')+' 23:59:59'
		if qiu=='I':
				endate =None

	col,data=query(date=idate,edate=endate,ctype=opcode,itype=tcode,dbname=dname)
	return (col,data,idate,endate)


def optype(ocode=0,name=mname):
	if ocode==0:
		print('exit')
	else:
		if ocode==1: 
			op=int(input('请选择记录类型: \n  1:固定收支记录;\n  2:非固定收支记录;\n  3:所有记录;\n 0:查询可用金额 \n  9：退出;\n>>>>'))
			if op==9:
				print('exit')
			if op==0:
				queryrecord(op,'A','Q',name)
			else:
				transactioncode=input('请输入类型代码 I 为收入 C 为支出 A 为所有:\n>>>>')
				queryrecord(op,transactioncode,'Q',name)
		
		elif ocode==2:#insert  
			op=int(input('请选择记录类型: \n  1:固定收支记录;\n  2:非固定收支记录;\n  9：退出;\n>>>>'))
			if op==9:
				print('exit')
			if op==1:
				transactioncode=input('请输入类型代码 I 为收入 C 为支出 A 为所有:\n>>>>')
				col,data,idate,endate=queryrecord(op,transactioncode,'I',name)
				

				if data:
					iu=input('存在已有记录! 请选择修改时间,还是更新。\n 1:修改时间；\n 2:更新当前数据；\n>>>>')
					if iu=='1':
						col,data,idate,endate=queryrecord(op,transactioncode,'I',name)
						if data2:
							oo=input('仍存在已有记录，建议您返回先进行记录查询，然后增加新记录\n 1:返回主目录；\n 2:更新当前数据；\n>>>>')
							if oo=='2':
								
								amountstr=input('请输入金额:')
								amount=float(amountstr)
								inputn=int(input('请输入持续月份:\n>>>>'))
								db.update(udate=idate,code=op,qtype=None,itype=transactioncode,amt=amount,dbname=name)
							else:
								main()
							
					if iu=='2':
						
						amountstr=input('请输入金额:')
						amount=float(amountstr)
						inputn=int(input('请输入持续月份:\n>>>>'))
						update(udate=idate,code=op,qtype=None,itype=transactioncode,amt=amount,dbname=name)
				else:
					
					amountstr=input('请输入金额:')
					amount=float(amountstr)
					inputn=int(input('请输入持续月份:\n>>>>'))
					insert(code=op,date=idate,itype=transactioncode,cycle=inputn,amt=amount,dbname=name)
					
			if op==2:
				transactioncode=input('请输入类型代码 I 为收入 C 为支出 A 为所有:\n>>>>')
				col,data,idate,endate=queryrecord(op,transactioncode,'I',name)
				
				if data:
					iu=input('存在已有记录! 请选择修改时间,还是更新。\n 1:修改时间；\n 2:更新当前数据；\n>>>>')
					if iu=='1':
						col,data,idate,endate=queryrecord(op,transactioncode,'I',name)
						if data2:
							oo=input('仍存在已有记录，建议您返回先进行记录查询，然后增加新记录\n 1:返回主目录；\n 2:更新当前数据；\n>>>>')
							if oo=='2':
								
								amountstr=input('请输入金额:')
								amount=float(amountstr)
							else:
								main()
					if iu=='2':
						
						amountstr=input('请输入金额:')
						amount=float(amountstr)
						update(udate=idate,code=op,qtype=None,itype=transactioncode,amt=amount,dbname=name)
					
				else:
					
					amountstr=input('请输入金额:')
					amount=float(amountstr)
					insert(code=op,date=idate,itype=transactioncode,cycle=0,amt=amount,dbname=name)
			
				
		elif ocode==3: #delete
			op=int(input('请选择记录类型: \n  1:固定收支记录;\n  2:非固定收支记录;\n   9：退出;\n>>>>'))
			if op==9:
				print('exit')
			else:
				transactioncode=input('请输入类型代码 I 为收入 C 为支出 A 为所有:\n>>>>')
				col,data,idate,endate=queryrecord(op,transactioncode,'D')
				delete (code=op,sdate=idate,edate=endate,ctype=transactioncode,dbname=name)
		elif ocode==4: #update
			op=int(input('请选择记录类型: \n  1:固定收支记录;\n  2:非固定收支记录;\n 3:所有记录; \n9：退出;\n>>>>'))
			if op==9:
				print('exit')
			else:
				opcode=int(input('请选择搜索条件(时间为必填项)1:只查询收入记录;\n 2：只查询支出记录;\n 3：查询特定金额;\n 0:跳过;\n>>>>>>> '))
				if opcode==1:
					trancode='I'
					queryamount=None
				elif opcode==2:
					trancode='C'
					queryamount=None
				elif opcode==3:
					queryamount=float(input('请输入要查询的金额:'))
					trancode='A'
				else: 
					trancode='A'
					queryamount=None
					
				col,data,idate,endate=queryrecord(op,trancode,'Q',name)
				if data:
					transactioncode=input('请输入更改后的类型代码： I 为收入 C 为支出 A 为忽略:\n>>>>')
					amountstr=input('请输入更改后金额:')
					amount=float(amountstr)
					if op==2:
						ucycle=None
					if op==1 or op==3:
						inputcycle=int(input('请输入持续月份, 如无变动则输入0:\n>>>>'))
						if inputcycle==0:
							ucycle=None
						else:
							ucycle=inputcycle
						
					update(udate=idate,code=op,qtype=trancode,itype=transactioncode,qamt=queryamount,amt=amount,cycle=inputcycle,edate=endate,dbname=name)
				else:
					
					if endate is None:
						print('不存在记录！将直接新增记录！')
						insert(code=op,date=idate,itype=transactioncode,cycle=ucycle,amt=amount,dbname=name)

		else:
			return()

def main():
	try:
		strname=input("请输入用户名: (默认为0)\n >>>>>>")
		cpath=os.getcwd() 
		if strname=='0':
			cname='accounting'
			dname='accounting.db'
		else:
			cname=strname
			dname=strname+'.db'
			
		name=os.path.join(cpath, dname)
		if os.path.exists(name):#检测是否已经存在数据库，如果不存在则直接创建一个
			print('欢迎'+cname+'!!')
			table_check(name)
		else:
			initialize(name)
			
		opcodetype=int(input('欢迎使用财务统计功能!!!可以把固定的收入支出登记，保持记录明细后可自动计算可支配余额！\n==============================\n请选择操作类型,\n1:查询记录;\n2:新增记录;\n3:删除记录;\n4:修改记录;\n0:退出;\n >>>'))
		optype(opcodetype,name)
		opcodetypeloop=int(input('==============================\n是否还有其它操作？\n 1:查询记录;\n2:新增记录;\n3:删除记录;\n4:修改记录;\n0:退出;\n >>>'))
		while opcodetypeloop>0:
				optype(opcodetypeloop,name)
				opcodetypeloop=int(input('==============================\n是否还有其它操作？\n 1:查询记录;\n2:新增记录;\n3:删除记录;\n4:修改记录;\n0:退出;\n >>>'))

		print('感谢使用财务统计功能!!')
	except Exception as e:
		log_helper.info('主页面错误：'+ str(e.args))
		print('请检查输入是否错误！')

if __name__ == "__main__":
	main()
