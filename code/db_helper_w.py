# -*- coding: UTF-8 -*-
import os,pandas,sqlite3,re,calendar
import log_helper,dbop
from texttable import Texttable
from datetime import datetime
from dbop import dbase

#请选择操作类型,\n  1:固定收入支出; 2:非固定收入支出 ;3:查询特定日期的可用支出金额:\n>>>
#请输入操作类型，1:查询\n2:增改\n3:删除\n 0:退出
#创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
#创建在内存上面： conn = sqlite3.connect('"memory:')

#dbname='C:\\Users\\henry.zhangtj\\AppData\\Local\\Programs\\Python\\Python37\\b\\accounting.db'
#dbname=account


def table_check(dbname):
	table=('financial_detail',)
	tablet=('financial_dict,',)
	tables=('financial',)
	q="SELECT name FROM sqlite_master WHERE type='table';"
	with dbase(dbname) as db:	
		col,data=db.sqlite(q)
	if table not in data:
		initialize (dbname)
	if tablet not in data:
		initialize (dbname)
	if tables not in data:
		initialize (dbname)
		
		
def initialize (dbname):
		csql=("create table financial_detail(id INTEGER PRIMARY KEY autoincrement, cdate DATETIME , qtype TEXT ,specific_amount NUMBER(38,4));\n\
		create table financial_dict(id INTEGER PRIMARY KEY autoincrement, cdate DATETIME , qtype TEXT ,specific_amount NUMBER(38,4), cycle INTEGER);\n\
		create table financial(id INTEGER PRIMARY KEY autoincrement,dictid INTEGER,detailid INTEGER, cdate DATETIME , qtype TEXT ,specific_amount NUMBER(38,4));")
		with dbase(dbname) as db:
			db.execute(csql)


		
def delete (code,sdate,edate,ctype,dbname):
	if ctype.upper()=='A':
		st=''
	else:
		st="qtype='"+ctype.upper()+"' and "
	if edate:
		strudate=("cdate between '{0}' and '{1}' ").format(sdate,edate)
	else:
		strudate=("cdate = '{0}'  ").format(sdate)
		
	if code==1:
		table='financial_dict'
		i='dictid'
	elif code==2:
		table='financial_detail'
		i='detailid'
	alsql=("delete from financial where {3} in (select id from {0} where  {1} {2})").format(table,st,strudate,i)

	dsql =("delete from {0} where {1} {2}").format(table,st,strudate)

	#print('\n 执行的sql语句：'+alsql+'\n=====================')
	with dbase(dbname) as db:	
		db.sqlite(alsql)
		
	#print('\n执行的sql语句：'+dsql+'\n=====================')
	with dbase(dbname) as db:
		db.sqlite(dsql)
		
def add_months(strdate,months):
	date=datetime.strptime(strdate,'%Y-%m-%d %H:%M:%S')
	basnum = date.month - 1 + months
	year = date.year + basnum // 12
	month = basnum%12+1
	#month2 = (date.month+months%12) %12
	day = min(date.day,calendar.monthrange(year,month)[1])
	#a=date.replace(year=year, month=month, day=day)
	#b=date.replace(year=year, month=month2, day=day)
	return date.replace(year=year, month=month, day=day)
	
	
	
#插入单条数据
def insert(code,date,itype,cycle,amt,dbname): # code 1 means dict ,2 means detail ;itype i/c
	qtype=itype.upper()
	if qtype=='C':
		ramt=-1*amt
	if qtype=='I':
		ramt=amt
	
	
	if code==1:
		table='financial_dict'
		c=',cycle'
		strcycle=','+ str(cycle)
		colid='dictid'
		acycle=1
		addsql=''
		while acycle<=cycle-1:
			adate=add_months(date,acycle)
			addsql=addsql+("union all   \
			SELECT id, '{0}' as cdate , qtype, specific_amount  FROM {1}\
			WHERE id = (SELECT seq FROM sqlite_sequence WHERE NAME = '{2}')").format(adate,table,table)
			acycle=acycle+1
				
	elif code==2:
		table='financial_detail'
		c=''
		strcycle=''
		addsql=''
		colid='detailid'
	
	isqld=("INSERT INTO financial ({2}, cdate, qtype, specific_amount) \
		SELECT id, cdate, qtype, specific_amount  FROM {0}\
		WHERE id = (SELECT seq FROM sqlite_sequence WHERE NAME = '{1}')").format(table,table,colid)	
	isqla=isqld+addsql
	isql=("insert into {0} (cdate,qtype,specific_amount{5})values ('{1}','{2}',{3}{4})").format(table,date,qtype,ramt,strcycle,c)
	#print('\n 执行的sql语句：'+isql+'\n=====================')
	with dbase(dbname)	as db:
		db.sqlite(isql)
		
	#print('\n 执行的sql语句：'+isqla+'\n=====================')
	with dbase(dbname)	 as db:
		db.sqlite(isqla)
		
	
	
#查询
def query(date,edate,ctype,itype,dbname):  #itype I/N ;type=0 query sum ; type=1 query dict; type=2 query detail only ;type=3 query detail include dict
	if itype.upper() =='I':
		stritype= "and qtype='I' "
	elif itype.upper()=='C':
		stritype="and qtype='C' "
	else:
		stritype=''
	if ctype==0:
		a=['l']
		d=['f']
		qsql=("select sum(specific_amount) as Available_balance from financial where cdate<= '{0}' {1}").format(date,stritype)
		
		
	if ctype==1:
		a=['l','c','c','c','c']
		d=['i','t','t','f','i']
		if edate:#(endate is None ):
			qsql=("select id, cdate, qtype,specific_amount, cycle from financial_dict where cdate between '{0}' and '{1}' {2}").format(date,edate,stritype)

		else:# endate is not None :
			qsql=("select id, cdate, qtype,specific_amount, cycle from financial_dict where cdate='{0}' {1}").format(date,stritype)

	if ctype==2:
		a=['l','c','c','c']
		d=['i','t','t','f']
		if (edate is None ):
			qsql=("select id,cdate, qtype,specific_amount from financial_detail where cdate='{0}'{1}").format(date,stritype)
		elif edate is not None :
			qsql=("select id,cdate,qtype,specific_amount from financial_detail where cdate between '{0}' and '{1}'{2}").format(date,edate,stritype)

	if ctype==3:
		a=['l','l','l','c','c','c']
		d=['i','t','t','t','t','f']
		if (edate is None ):
			qsql=("select id,dictid,detailid,cdate, qtype,specific_amount from financial where cdate='{0}'{1}").format(date,stritype)
		elif edate is not None :
			qsql=("select id,dictid,detailid,cdate,qtype,specific_amount from financial where cdate between '{0}' and '{1}'{2}").format(date,edate,stritype)
	#print('\n 执行的sql语句：'+qsql+'\n=======')

	with dbase(dbname) as db:	
		col,data=db.sqlite(qsql)
		#print(col)
		#print(data)
		df=pandas.DataFrame(data=data,columns=col)
		tb=Texttable()
		tb.set_cols_align(a) 
		#tb.set_cols_valign(['m','m','m','m','m']) 
		tb.set_cols_dtype(d)
		tb.header(df.columns.get_values())
		tb.add_rows(df.values,header=False)
		tbout=(tb.draw()+'\n=======*********************************=========')
		return (col,data,tbout)

#update

def update(udate,code,qtype,itype,qamt,amt,cycle,edate,dbname):  #code=1 update dict; type=2 upadte detail ;
	try:
		ucol='specific_amount'
		if itype.upper()=='I':
			iamt=1*amt
			ucol2=",qtype= 'I' "
		elif itype.upper()=='C':
			iamt=-1*amt
			ucol2=",qtype= 'C' "
		else:
			abscode=1
			ucol2=""
			iamt=amt
			
		if edate:
			strudate=("cdate between '{0}' and '{1}' ").format(udate,edate)
		else:
			strudate=("cdate = '{0}'  ").format(udate)
		
		if qtype.upper() =='I':
			strqtype= "and qtype='I' "
		elif qtype.upper()=='C':
			strqtype="and qtype='C' "
		else:
			strqtype=''

		if qamt :
			strqamt='and specific_amount ='+srt(qamt)
			
		else:
			strqamt=''
			
		if code==1:
			table='financial_dict'
			if cycle:
				ucol2=ucol2+',cycle='+str(cycle)
			
			delete (code=1,sdate=udate,edate=edate,ctype=itype,dbname=dbname)
			
			insert(code=1,date=udate,itype=itype,cycle=cycle,amt=amt,dbname=dbname)
			
			
		if code==2:
			table='financial_detail'

			usql=(" update {0} set {1} = {2} {3} where {4} {5}{6} ").format(table,ucol,iamt,ucol2,strudate,strqtype,strqamt)
			with dbase(dbname) as db:
				db.sqlite(usql)
				
			usqla=(" update financial set {1} = {2} {3} where {4} {5}{6} ").format(table,ucol,iamt,ucol2,strudate,strqtype,strqamt)
			with dbase(dbname) as db:
				db.sqlite(usqla)
	except Exception as e:
		log_helper.info('更新错误：'+ str(e.args))