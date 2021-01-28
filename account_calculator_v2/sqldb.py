# -*- coding: UTF-8 -*-
import pandas,sqlite3,os,re
from texttable import Texttable
from datetime import datetime
#请选择操作类型,\n  1:固定收入支出; 2:非固定收入支出 ;3:查询特定日期的可用支出金额:\n>>>
#请输入操作类型，1:查询\n2:增改\n3:删除\n 0:退出
#创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
#创建在内存上面： conn = sqlite3.connect('"memory:')
#dbname='accounting'

account='C:\\Users\\henry.zhangtj\\AppData\\Local\\Programs\\Python\\Python37\\b\\accounting.db'
def escript(dbname,sql):
	connect=sqlite3.connect(dbname)
	cursor=connect.cursor()
	cursor.executescript(sql)
	out= cursor.fetchall()
	connect.commit()
	cursor.close()
	connect.close()
	return (out)

#C:\\Users\\henry.zhangtj\\AppData\\Local\\Programs\\Python\\Python37\\accounting.db
def sqlite (dbname ,sql):
	connect=sqlite3.connect(dbname)
	cursor=connect.cursor()
	cursor.execute(sql)
	out=[]
	if cursor.description:
		out2= cursor.fetchall()
		out=[tuple[0] for tuple in cursor.description]
		#if out2:
		#	for i,s in enumerate (out2[0]):
		#		s=cursor.description[i][0]
		#		out.append(s)
		#else:
		#	out=[tuple[0] for tuple in cursor.description]

	else:
		out2 = cursor.rowcount
		
	connect.commit()
	cursor.close()
	connect.close()
	return (out,out2)

#删除数据
def delete (code,sdate,edate,ctype):
	if ctype.upper()=='A':
		st=''
	else:
		st='qtype='+ctype.upper()+' and '
	
	if code==1:
		table='financial_dict'
		i='dictid'
	elif code==2:
		table='financial_detail'
		i='detailid'
	alsql=("delete from financial where {4} in(select id from {0} where {1} cdate between '{2}' and '{3}')").fromat(table,st,sdate,edate,i)
	
	dsql=("delete from {0}where {1} cdate between '{2}' and '{3}'").fromat(table,st,sdate,edate)
	
	print('\n 执行的sql语句：'+alsql+'\n=====================')
	sqlite('accounting',alsql)
	print('\n执行的sql语句：'+dsql+'\n=====================')
	sqlite(account,dsql)

	
#插入单条数据
def insert(code,date,itype,cycle,amt): # code 1 means dict ,2 means detail
	qtype=itype.upper()
	if code==1:
		table='financial_dict'
		c=',cycle'
		strcycle=','+ str(cycle)
		colid='dictid'
		acycle=cycle-1
		addsql=''
		while acycle>=1:
			addsql=addsql+("union all   \
			SELECT id, datetime(cdate,'+{0} months'), qtype, specific_amount  FROM {1}\
			WHERE id = (SELECT seq FROM sqlite_sequence WHERE NAME = '{2}')").format(acycle,table,table)
			acycle=acycle-1
				
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
	isql=("insert into {0} (cdate,qtype,specific_amount{5})values ('{1}','{2}',{3}{4})").format(table,date,qtype,amt,strcycle,c)
	print(isql+'\n=====================')
	sqlite('accounting',isql)
	
	print(isqld+'\n=====================')
	sqlite(account,isqla)
	
	
#查询
def query(date,edate,ctype,itype):  #itype I/N ;type=0 query sum ; type=1 query dict; type=2 query detail only ;type=3 query detail include dict
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
	#print(qsql)

        
	col,data=sqlite(account,qsql)
	#print(col)
	#print(data)
	df=pandas.DataFrame(data=data,columns=col)
	tb=Texttable()
	tb.set_cols_align(a) 
	#tb.set_cols_valign(['m','m','m','m','m']) 
	tb.set_cols_dtype(d)
	tb.header(df.columns.get_values())
	tb.add_rows(df.values,header=False)
	print(tb.draw()+'\n=======*********************************=========')
	return (col,data)

#update

def update(udate,code,qtype,itype,amt):  #code=1 update dict; type=2 upadte detail ;
	if qtype.upper() =='I':
		strqtype= "and qtype='I' "
	elif qtype.upper()=='C':
		strqtype="and qtype='C' "
	else:
		strqtype=''
	strityp=itype.upper()
	if itype:
		ucol='qtype'
	else:
		itype=''
		ucol=' ='
	if amt :
		qamt=', specific_amount ='
		stramt=amt
	else:
		qamt=''
		stramt=''
	if code==1:
		table='financial_dict'
		ucol='qtype ='
		ccol=''

	if code==2:
		table='financial_detail'
		ucol='qtype ='

	usql=(" update {0} set {1} = '{2}'{3} {4}where cdate='{5}' {6} ").format(table,ucol,itype,qamt,stramt,udate)
	sqlite(account,usql)
