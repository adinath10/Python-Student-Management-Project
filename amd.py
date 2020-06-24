from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import numpy as np
import matplotlib.pyplot as plt

root=Tk()
root.title("S. M. S.")
root.geometry("600x500+500+100")
root.resizable(0,0)
root.configure(background="peach puff")
import bs4
import requests

res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")

soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})

t1=quote['alt']
print(t1)


import socket
import requests
try:
	city="mumbai"
	socket.create_connection(("www.google.com",80))
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+city
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address=a1+a2+a3
	res1=requests.get(api_address)
	data=res1.json()
	main=data['main']
	temp=main['temp']
	print(temp)

except  OSError:
	print("check network")






def f1():
	root.withdraw()
	addst.deiconify()

def f2():
	addst.withdraw()
	root.deiconify()

def f3():
	root.withdraw()
	viewst.deiconify()
	import cx_Oracle
	con= None
	cursor=None
	try:
		con=cx_Oracle.connect("System/abc123")
		cursor = con.cursor()
		sql="select rno,name,marks from s1"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg=""
		for d in data:
			msg+="r: "+str(d[0])+"  n: "+str(d[1])+"  mrks: "+str(d[2])+"\n"
		stData.insert(INSERT,msg)
	except cx_Oracl.DatabaseError as e:
		print("some issue",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
def f4():
	viewst.withdraw()
	root.deiconify()
	stData.delete('1.0',END) #delete previous data from scrolled text	


def f6():
	root.withdraw()
	updatest.deiconify()

def f7():
	root.withdraw()
	deletest.deiconify()


def f5():
	import cx_Oracle
	cursor=None
	con=None
	try:
		con=cx_Oracle.connect("system/abc123")
		rno=int(entRno.get())
		name=entName.get()
		marks=int(entMarks.get())
		if rno <=0 :
			messagebox.showerror("Error","please enter positive integers")
			entRno.delete(0,END)
			entRno.focus()
			
		elif name.isalpha()== False:
			messagebox.showerror("Error","please enter letters only ")
			entName.delete(0,END)
			entName.focus()
			
		elif marks >100 or marks <0 :
			messagebox.showerror("Error","marks should be between 0 and 100 ")
			entMarks.delete(0,END)
			entMarks.focus()
		
		else:	
			cursor=con.cursor()
			sql="insert into  s1 values('%d','%s','%d')"
			args=(rno,name,marks)
			cursor.execute(sql % args)
			con.commit()
			msg=str(cursor.rowcount)+ "records inserted "
			messagebox.showinfo("sahi ",msg)
			entRno.delete(0,END)
			entName.delete(0,END)
			entMarks.delete(0,END)
			entRno.focus()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("galat ",e)
		con.rollback()

	except ValueError:
		messagebox.showerror("Error","Please enter integers only")
		con.rollback()
		entRno.delete(0,END)
		entMarks.delete(0,END)
		entRno.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close() 
			
def f8():
	import cx_Oracle
	cursor=None
	con=None
	try:
		con=cx_Oracle.connect("system/abc123")
		rno=int(dentRno.get())
		cursor=con.cursor()
		sql="delete from  s1 where rno = '%d'"
		args=(rno)
		cursor.execute(sql % args)
		con.commit()
		if cursor.rowcount==0:
			messagebox.showinfo("error","Record does not exist")
		else:
			msg=str(cursor.rowcount)+ "  records deleted"
			messagebox.showinfo("sahi ",msg)
		dentRno.delete(0,END)
		dentRno.focus()
		
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("galat ","Record does not exist")
		con.rollback()
		dentRno.delete(0,END)
		dentRno.focus()
	except ValueError:
		messagebox.showerror("Error","Please enter integers only")
		con.rollback()
		dentRno.delete(0,END)
		dentRno.focus()
def f9():
	import cx_Oracle
	cursor=None
	con=None
	try:
		con=cx_Oracle.connect("system/abc123")
		rno=int(uentRno.get())
		name=uentName.get()
		marks=int(uentMarks.get())
		if rno <=0 and rno.isdigit()== False:
			messagebox.showerror("Error","please enter positive integers")
			uentRno.delete(0,END)
			uentRno.focus()
			
		elif name.isalpha()== False:
			messagebox.showerror("Error","please enter letters only ")
			uentName.delete(0,END)
			uentName.focus()
			
		elif marks >100 or marks <0 :
			messagebox.showerror("Error","marks should be between 0 and 100 ")
			uentMarks.delete(0,END)
			uentMarks.focus()
		
		else:	
			cursor=con.cursor()
			sql="update s1 set name='%s' , marks='%d' where rno='%d'"
			args=(name,marks,rno)
			cursor.execute(sql % args)
			con.commit()
			msg=str(cursor.rowcount)+ "records updated "
			if cursor.rowcount == 0:
				messagebox.showerror("Error","Record does not exist")
			else:
				messagebox.showinfo("Info ",msg)
			uentRno.delete(0,END)
			uentName.delete(0,END)
			uentMarks.delete(0,END)
			uentRno.focus()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("galat ","Record does not found")
		con.rollback()

	except ValueError:
		messagebox.showerror("Error","Please enter integers only")
		con.rollback()
		uentRno.delete(0,END)
		uentMarks.delete(0,END)
		uentRno.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close() 

def last(n): 
    return n[0]   
       
def sort(tuples): 
    return sorted(tuples, key = last) 
   

			
def f10():
	import numpy as np
	import matplotlib.pyplot as plt
	import cx_Oracle
	cursor=None
	con=None
	
	try:
		x1,x2,x3=[],[],[]
		list,final=[],[]
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select marks,rno,name from s1"
		cursor.execute(sql)
		row = cursor.fetchone()
		while row != None:
			print(row)
			list.append(row)
			row=cursor.fetchone()
		print(list)
		print(sort(list))
		list=sort(list)
		l=len(x3)
		for i in range(0,5):
			y=list[l-1]
			final.append(y)
			l=l-1
		print("final",final)
		for i in final:
			x1.append(i[0])
			x2.append(i[1])
			x3.append(i[2])
		x=np.arange(len(x3))
		plt.bar(x,x1,label="marks",color='r')
		plt.title("Graph")
		plt.xlabel('Name of the students')
		plt.ylabel('Marks of the students ')
		plt.xticks(x,x3)
		plt.grid()
		plt.legend()
		plt.show()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("galat ","Record does not exist")
		con.rollback()()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close() 
		
def f11():
	deletest.withdraw()
	root.deiconify()

	
		
def f12():
	updatest.withdraw()
	root.deiconify()
	
	
	

btnAdd=Button(root,text="Add",font=("arial",18,"bold"),width=10,command=f1)
btnAdd.configure(background="indian red")
btnView=Button(root,text="View",font=("arial",18,"bold"),width=10,command=f3)			
btnUpdate=Button(root,text="Update",font=("arial",18,"bold"),width=10,command=f6)
btnDelete=Button(root,text="Delete",font=("arial",18,"bold"),width=10,command=f7)			
btnGraph=Button(root,text="Graph",font=("arial",18,"bold"),width=10, command=f10)
entQuote=Entry(root,width=65,font=("arial",10,"bold"))
entQuote.insert(850, t1 )     
lblQuote=Label(root,text="Quote of the day: ",font=("arial",10,"bold"))
lblQuote.configure(background="peach puff")
entTemp=Entry(root,font=("arial",10,"bold"),width=65)
x=str(temp)+chr(176)+"C"
entTemp.insert(850,x)

lblTemp=Label(root,text="Temperature:     ",font=("arial",10,"bold"))

lblTemp.configure(background="peach puff")

btnView.configure(background="indian red")
btnUpdate.configure(background="indian red")
btnDelete.configure(background="indian red")
btnGraph.configure(background="indian red")
btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)

lblTemp.place(x=10,y=420)
entTemp.place(x=120,y=420)
lblQuote.place(x=10,y=400)
entQuote.place(x=120,y=400)

addst=Toplevel(root)
addst.title("Add Students")
addst.geometry("500x500+500+100")
addst.resizable(0,0)
addst.withdraw()
lblRno=Label(addst,text="enter rno ",font=("arial",18,"bold"))
entRno=Entry(addst,font=("arial",18,"bold"))
lblName=Label(addst,text="enter Name ",font=("arial",18,"bold"))
entName=Entry(addst,font=("arial",18,"bold"))
lblMarks=Label(addst,text="enter Marks ",font=("arial",18,"bold"))
entMarks=Entry(addst,font=("arial",18,"bold"))
btnAddSave = Button(addst,text="Save",font=("arial",18,"bold"),width=10,command=f5)
btnAddBack = Button(addst,text="Back",font=("arial",18,"bold"),width=10,command=f2)

lblRno.pack(pady=5)
entRno.pack(pady=5)
lblName.pack(pady=5)
entName.pack(pady=5)
lblMarks.pack(pady=5)
entMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

lblMarks.configure(background="peach puff")
lblName.configure(background="peach puff")
lblRno.configure(background="peach puff")
btnAddBack.configure(background="indian red")
btnAddSave.configure(background="indian red")
viewst=Toplevel(root)
viewst.title("View Students")
viewst.geometry("500x500+500+100")
viewst.withdraw()

stData=scrolledtext.ScrolledText(viewst, width=40,height=20, wrap=WORD)
btnViewBack =Button(viewst, text="Back",font=("arial",18,"bold"),command=f4,width=15)

stData.place(x=80,y=30)
btnViewBack.place(x=140,y=400)
btnViewBack.configure(background="indian red")

updatest=Toplevel(root)
updatest.title("Update Students")
updatest.geometry("500x500+500+100")
updatest.resizable(0,0)
updatest.withdraw()
ulblRno=Label(updatest,text="enter rno ",font=("arial",18,"bold"))
uentRno=Entry(updatest,font=("arial",18,"bold"))
ulblName=Label(updatest,text="enter Name ",font=("arial",18,"bold"))
uentName=Entry(updatest,font=("arial",18,"bold"))
ulblMarks=Label(updatest,text="enter Marks ",font=("arial",18,"bold"))
uentMarks=Entry(updatest,font=("arial",18,"bold"))
btnUpdateSave = Button(updatest,text="Save",font=("arial",18,"bold"),width=10,command=f9)
btnUpdateBack = Button(updatest,text="Back",font=("arial",18,"bold"),width=10,command=f12)

ulblRno.pack(pady=5)
uentRno.pack(pady=5)
ulblName.pack(pady=5)
uentName.pack(pady=5)
ulblMarks.pack(pady=5)
uentMarks.pack(pady=10)
btnUpdateSave.pack(pady=10)
btnUpdateBack.pack(pady=10)

ulblRno.configure(background="peach puff")

ulblName.configure(background="peach puff")

ulblMarks.configure(background="peach puff")

btnUpdateSave.configure(background="indian red")
btnUpdateBack.configure(background="indian red")


deletest=Toplevel(root)
deletest.title("Delete Students")
deletest.geometry("500x500+500+100")
deletest.resizable(0,0)
deletest.withdraw()
dlblRno=Label(deletest,text="enter rno ",font=("arial",18,"bold"))
dentRno=Entry(deletest,font=("arial",18,"bold"))
btnDeleteSave = Button(deletest,text="Save",font=("arial",18,"bold"),width=10,command=f8)
btnDeleteBack = Button(deletest,text="Back",font=("arial",18,"bold"),width=10,command=f11)

dlblRno.pack(pady=5)
dentRno.pack(pady=5)
btnDeleteSave.pack(pady=10)
btnDeleteBack.pack(pady=10)

dlblRno.configure(background="peach puff")
btnDeleteSave.configure(background="indian red")
btnDeleteBack.configure(background="indian red")


graphst=Toplevel(root)
graphst.title("Graph of Students")
graphst.geometry("500x500+500+100")
graphst.resizable(0,0)
graphst.withdraw()

btngraphBack = Button(graphst,text="Back",font=("arial",18,"bold"),width=10,command=f2)
btngraphBack.pack(pady=10)
addst.configure(background="peach puff")
updatest.configure(background="peach puff")
deletest.configure(background="peach puff")
viewst.configure(background="peach puff")

root.mainloop()