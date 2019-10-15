# coding=utf-8
import tkinter as tk,os,pandas,re
from tkinter import ttk,messagebox,scrolledtext,Menu
from datetime import datetime
from db_helper import initialize,table_check
from texttable import Texttable
from db_helper_w import insert,update,delete,query,initialize,table_check

#OTYP={'查询记录':1,'新增记录':2,'删除记录':3,'修改记录':4,'固定收支记录':5,'非固定收支记录':6,'所有记录':7,'查询可用金额':8}


class user_login(tk.Tk):
	def __init__(self):
		super().__init__()
		self.logwin()

	def logwin(self):
		self.title('用户登陆')
		page=tk.Frame(self).grid(column=0,row=0,pady=5,padx=5)
		self.name=tk.StringVar()
		tk.Label(page,text='请先登陆用户').grid(row=0,column=0,sticky='N'+'E'+'S'+'W',columnspan=2,pady=10)
		tk.Label(page,text='请输入用户名:').grid(row=1,column=0,sticky='E')
		tk.Entry(page,width=15,textvariable=self.name).grid(row=1,column=1,sticky='W')
		tk.Button(page,text='确定',width=10,command=self.nextstep).grid(row=3,column=0,sticky='E',padx=10,pady=30)
		tk.Button(page,text='退出',width=10,command=quit).grid(row=3,column=1,sticky='W',padx=10,pady=30)
		#for child in page.winfo_children(): 
		#	child.grid_configure(padx=3,pady=1)
	def nextstep(self):
		userinfo=self.name.get()
		#user=self.name.get()
		if userinfo is None or userinfo=='':
			messagebox.showwarning('Error Box', '错误：请先登陆！')
			self.logwin()
		else:
			cpath=os.getcwd()
			dname=userinfo+'.db'
			dbfname=os.path.join(cpath, dname)
			if os.path.exists(dbfname):
				table_check(dbfname)
			else:
				initialize(dbfname)
			
			self.destroy()#
			win=main_win(dbfname)
			win.mainloop()

class main_win(tk.Tk,object):
	def __init__(self,user):
		super().__init__()
		self.title('Henry财务统计')
		self.resizable(0,0)
		self.datbase_url=user
		self.optype=0		#记录类型代码
		self.opcodetype=0	#操作类型代码
		self.trancode='N'	#交易类型代码
		self.startdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.money=0.000
		self.mw()
	def dict_q(self,var):
		return{'查询记录':1,'新增记录':2,'删除记录':3,'修改记录':4,'固定收支记录':1,'非固定收支记录':2,'所有记录':3,'查询可用金额':0,'收入':'I','支出':'C','所有':'A'}.get(var,'NULL')

	def mw(self):
		self.mtable=tk.Frame(self).grid(row=0,column=0)

		
		tk.Label(self.mtable, text="请选择操作类型:").grid(row=1,column=0,sticky='W',columnspan=4)
		self.quvalues=['查询记录', '新增记录','删除记录','修改记录']
		self.vint=tk.IntVar()
		self.vint.set(99)
		for ccount in range(4):
			query_type=tk.Radiobutton(self.mtable,text=self.quvalues[ccount],variable=self.vint,value=ccount,command=self.QueryType)
			query_type.grid(row=2,column=ccount, sticky=tk.W)
			
		#record select
		tk.Label(self.mtable,text='请选择记录类型:').grid(row=3,column=0,sticky='W',columnspan=4)
		# Radiobutton list
		self.values = ["固定收支记录", "非固定收支记录", "所有记录"]
		# create three Radiobuttons using one variable
		self.radVar = tk.IntVar()
		# Selecting a non-existing index value for radVar
		self.radVar.set(99)    
		# Creating all three Radiobutton widgets within one loop
		for col in range(3):
			curRad = tk.Radiobutton(self.mtable, text=self.values[col], variable=self.radVar, value=col, command=self.CodeCall)
			curRad.grid( row=4,column=col, sticky=tk.W)
		


		#date insert
		self.sdate=tk.StringVar()
		self.edate=tk.StringVar()
		self.monVar = tk.StringVar()
		self.qmonVar = tk.StringVar()
		self.months =tk.StringVar()
		
		#嵌套区域
		ucondition=ttk.LabelFrame(self.mtable,text='查询条件')
		ucondition.grid(row=5,column=0,columnspan=4,pady=5,sticky='W')
		
		tk.Label(ucondition,text='请输入开始日期(格式为2019-06-01 00:00:00,当前时间请直接输入D,留空默认为当年1月1号):').grid(row=6,column=0,columnspan=4,sticky='W')
		tk.Entry(ucondition,width=35,textvariable=self.sdate).grid(row=7,column=0,sticky='W',padx=2,columnspan=4)
		tk.Label(ucondition,text='请输入截止日期(格式为2019-12-01默认截止到该日期23:59:59,当前日期请直接输入D,跳过请留空):').grid(row=8,column=0,columnspan=4,sticky='W')
		tk.Entry(ucondition,width=35,textvariable=self.edate).grid(row=9,column=0,sticky='W',padx=2,columnspan=4)

		tk.Label(ucondition,text='请输入查询金额:').grid(row=13,column=0,sticky='W')
		tk.Entry(ucondition,width=20,textvariable=self.qmonVar).grid(row=13,column=1,sticky='W')
		#second radiobutton list
		tk.Label(ucondition,text='请选择要查询的交易类型:').grid(row=10,column=0,sticky='W',columnspan=4)#,pady=10
		valuest = [("收入",'I'), ("支出",'C'),("所有",'A') ]
		self.tcVar = tk.StringVar()
		self.tcVar.set('A') 
		col2=0
		for cstr,ccode in valuest:
			transactioncode = tk.Radiobutton(ucondition, text=cstr, variable=self.tcVar, value=ccode, command=self.TcodeCall)
			transactioncode.grid( row=11, column=col2,sticky=tk.W)
			col2 =col2 +1
			
		#变更输入区域
		tk.Label(self.mtable,text='请输入具体金额:').grid(row=14,column=0,sticky='W',pady=4)
		tk.Entry(self.mtable,width=20,textvariable=self.monVar).grid(row=14,column=1,sticky='W')
		
		tk.Label(self.mtable,text='请输入持续月份():').grid(row=14,column=2,sticky='W')
		tk.Entry(self.mtable,width=20,textvariable=self.months).grid(row=14,column=3,sticky='W')

		
		tk.Label(self.mtable,text='请选择修改后的交易类型，不变更请不要选择:').grid(row=12,column=0,sticky='W',columnspan=4)#,pady=10
		valuest = [("收入",'I'), ("支出",'C'),("所有",'A')]
		self.qtcVar = tk.StringVar()
		self.qtcVar.set('O') 
		col3=0
		for qcstr,qccode in valuest:
			qtctioncode = tk.Radiobutton(self.mtable, text=qcstr, variable=self.qtcVar, value=qccode, command=self.CcodeCall)
			qtctioncode.grid( row=13, column=col3,sticky=tk.W)
			col3 =col3 +1
			
		#text show all print 
		self.scr = scrolledtext.ScrolledText(self.mtable, width=80, height=20, wrap=tk.WORD)
		self.scr.grid(row=15,column=0, columnspan=4)

		#退出按钮self.logout=
		tk.Button(self.mtable,text='退出',width=10,command=quit).grid(row=25,column=2,stick='W',padx=5,pady=10)
		#直接查询可用金额按钮
		tk.Button(self.mtable,text='查询可用金额',width=10,command=self.goto_optype).grid(row=25,column=0,padx=5,pady=30)
		#提交按钮
		tk.Button(self.mtable,text='提交',width=10,command=self.goto_sumbit).grid(row=25,column=1,padx=5,pady=30)
		#清屏按钮
		tk.Button(self.mtable,text='重置',width=10,command=self.reset).grid(row=25,column=3,padx=5,pady=30)
	def reset(self):
		self.scr.delete('1.0','end')
		self.qtcVar.set('O') 
		self.tcVar.set('A') 
		self.sdate.set('')
		self.edate.set('')
		self.monVar.set('')
		self.qmonVar.set('')
		self.months.set('')
		self.vint.set(99)
		self.radVar.set(2)
		
	def QueryType(self):
		#nu=self.vint.get()
		#su=self.quvalues[nu]
		#self.opcodetype=self.dict_q(su)
		self.opcodetype=self.dict_q(self.quvalues[self.vint.get()])
		self.scr.insert(tk.INSERT, '选择的操作类型是:'+str(self.opcodetype) +'\n')
		
	# Radiobutton callback function
	def CodeCall(self):
		s=self.radVar.get()
		st=self.values[s]
		self.optype=self.dict_q(st)
		
		self.scr.insert(tk.INSERT, '选择的记录类型是:'+str(s)+';'+str(self.optype) +'\n')
		
	def TcodeCall(self):
		self.trancode=self.tcVar.get()
		self.scr.insert(tk.INSERT, '选择的交易类型代码:'+self.trancode +'\n')
		
	def CcodeCall(self):
		self.Ctrancode=self.qtcVar.get()
		self.scr.insert(tk.INSERT, '变更后的交易类型代码:'+self.Ctrancode +'\n')

	def is_valid_date(self,datestr):
		#'''判断是否是一个有效的日期字符串'''
		try:
			datetime.strptime(datestr,'%Y-%m-%d')
			return True
		except:
			return False
	
	def goto_sumbit(self):
		if self.opcodetype in (1,2,3,4):
			if self.optype in (1,2,3):
				if self.monVar.get()=='' or self.monVar.get() is None:
					self.money=0.00
				else:
					self.money=float(self.monVar.get().replace(',',''))
				#self.money=float(amountstr)
				
				if self.qmonVar.get()=='' or self.qmonVar.get() is None:
					qamountstr='0.00'
				else:
					qamountstr=self.qmonVar.get()
				queryamount=float(qamountstr.replace(',',''))#queryamount#查询金额条件
				
				if self.months.get()=='' or self.months.get() is None:
					cyclei=0
				else:
					cyclei=int(self.months.get())#变更后的月份
					
				if self.opcodetype==1:
					col,data,idate,endate,out=self.queryrecord(self.optype,self.trancode,'Q',self.datbase_url)
					self.scr.insert(tk.INSERT,out+'\n=======*********************************=========\n')
					self.scr.insert(tk.INSERT,str(idate)+'\n'+str(endate)+'\n=======*********************************=========\n')
				elif self.opcodetype==2:
					col,data,idate,endate,out=self.queryrecord(self.optype,self.trancode,'I',self.datbase_url)
					if data :
						messagebox.showwarning('Error', '已有相同时间的数据！请更改时间或选择更新数据！')
						self.scr.insert(tk.INSERT,out+'\n=======*********************************=========\n')
					else:
						if self.trancode in ('I','C','i','c'):
							insert(code=self.optype,date=idate,itype=self.trancode,cycle=cyclei,amt=self.money,dbname=self.datbase_url)
							#self.scr.insert(tk.INSERT,str(idate)+'\n'+str(endate)+'\n 月份是：'+str(cyclei)+'\n 金额是：'+str(self.money)+'\n=======*********************************=========\n')
						else:
							messagebox.showwarning('Error', '请选择交易类型！')
				elif self.opcodetype==3:
					if self.trancode in ('I','C','i','c'):
						col,data,idate,endate,out=self.queryrecord(self.optype,self.trancode,'D',self.datbase_url)
						self.scr.insert(tk.INSERT,'以下数据被删除：\n'+out+'\n=======*********************************=========\n')
						delete (code=self.optype,sdate=idate,edate=endate,ctype=self.trancode,dbname=self.datbase_url)
					else:
						messagebox.showwarning('Error', '请选择交易类型！')
				elif self.opcodetype==4:
						
					col,data,idate,endate,out=self.queryrecord(self.optype,self.trancode,'Q',self.datbase_url)
					if data:
						self.scr.insert(tk.INSERT,out+'\n=======*********************************=========\n')
						self.scr.insert(tk.INSERT,str(idate)+'\n'+str(endate)+'\n更改交易类型为'+Ctrancode+'\n 金额是：'+str(self.money)+'\n=======*********************************=========\n')
						
						update(udate=idate,code=self.optype,qtype=self.trancode,itype=self.Ctrancode,qamt=queryamount,amt=self.money,cycle=cyclei,edate=endate,dbname=self.datbase_url)
					else:
						messagebox.showwarning('information', '未查询到结果，将直接插入数据！')
						insert(code=self.optype,date=idate,itype=self.trancode,cycle=cyclei,amt=self.money,dbname=self.datbase_url)
				else:
					messagebox.showwarning('Error', '请选择操作类型！')
			else :
				messagebox.showwarning('Error', '请选择记录类型！')
		else:
			messagebox.showwarning('Error', '请选择操作类型！')
					
	def goto_optype(self):
		col,data,idate,endate,out=self.queryrecord(0,'A','Q',self.datbase_url)
		self.scr.insert(tk.INSERT,out+'\n=======*********************************=========\n')
		self.scr.insert(tk.INSERT,str(idate)+'\n'+str(endate)+'\n=======*********************************=========\n')
		return (col,data)

	def is_valid_datetime(self,datestr):
		#'''判断是否是一个有效的日期字符串'''
		try:
			datetime.strptime(datestr,'%Y-%m-%d %H:%M:%S')
			return True
		except:
			return False
	def queryrecord (self,opcode,tcode,qiu,dname):
		idatestr=self.sdate.get()
		if idatestr.upper()=='D' :
			self.startdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		elif idatestr.upper()=='Y'or idatestr==''or idatestr is None:
			a=datetime.now()
			self.startdate=a.replace(year=a.year, month=1, day=1).strftime('%Y-%m-%d %H:%M:%S')
		else:
			#it=bool(re.search('\d{1,2}:\d{1,2}:\d{1,2}&',idatestr))
			itd=self.is_valid_date(idatestr)
			it=self.is_valid_datetime(idatestr)
			if it==True:
				self.startdate=datetime.strptime(idatestr,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
			elif it==False and itd==True:
				self.startdate=datetime.strptime(idatestr,'%Y-%m-%d').strftime('%Y-%m-%d')+' 00:00:00'#time.strptime(idatestr,'%Y-%m-%d')
			else:
				messagebox.showwarning('Error', '请输入正确日期时间！')

		if opcode==0:
			if idatestr=='' or idatestr is None:
				qdate =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			else:
				qdate=self.startdate
			endate =None
		else:
			qdate=self.startdate
			if (qiu=='Q' or qiu=='D'):
				endt=self.edate.get() #input('请输入截止日期 (格式为2019-12-01默认截止到该日期23:59:59) ,输入d当前日期,查询可用请按0跳过:\n>>>>')
				if endt.upper()=='D':
					endate=datetime.now().strftime('%Y-%m-%d')+' 23:59:59'
				elif endt=='0' or endt=='':
					endate =None
				else:
					endate=datetime.strptime(endt,'%Y-%m-%d').strftime('%Y-%m-%d')+' 23:59:59'
			if qiu=='I':
					endate =None

		col,data,out=query(date=qdate,edate=endate,ctype=opcode,itype=tcode,dbname=dname)
		return (col,data,qdate,endate,out)



	def delete_table(self):
		# Adding a Combobox
		self.book=tk.StringVar()
		bookChosen= ttk.Combobox(self.mtable,width=10,textvariable=self.book)
		bookChosen['values'] = ('请选择','查询记录', '新增记录','删除记录','修改记录')
		bookChosen.grid(column=0, row=2,sticky='W')
		bookChosen.current(0)  #设置初始显示值，值为元组['values']的下标
		bookChosen.config(state='readonly')  #设为只读模式
		bookChosen.bind("<<ComboboxSelected>>", self.opcodefun)#选择下拉选项时触发事件
	def opcodefun(self,event):
		
		comsel=self.book.get()
		self.opcodetype=self.dict_q(comsel)
		#OTYP.get(comsel,'NULL')
		if comsel in('查询记录', '新增记录','删除记录','修改记录'):

			strname=self.username
			if strname is None or strname=='':
				messagebox.showwarning('Error Box', '错误：请先登陆！')
			else:
				self.scr.insert(tk.INSERT, self.username +':已经登陆'+'操作码是：'+comsel +str(self.opcodetype)+'\n')
				messagebox.showinfo(title=comsel, message='welcome,'+strname+'!!/n 请输入日期')
				#outlist=self.get_choice()
				#self.sop.config(text=outlist)
		
if __name__=='__main__':
	root=user_login()
	root.mainloop()
