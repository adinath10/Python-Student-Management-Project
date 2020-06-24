#wapp to use gui and database 

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from cx_Oracle import *
import numpy as np
import matplotlib.pyplot as plt

import bs4
import requests

res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")

soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})

t1=quote['alt']
#print(t1)

import socket
import requests
try:
	city="MUMBAI"
	socket.create_connection(("www.google.com",80))
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+city
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address=a1+a2+a3
	res1=requests.get(api_address)
	data=res1.json()
	main=data['main']
	temp=main['temp']
	#print(temp)
	
	#print(city)

except  OSError:
	print("check network")


root = Tk()
root.title("S . M . S")
root.geometry("590x510+200+200")
root.configure(background = "black")

def f1():
	root.withdraw()
	adst.deiconify()

def f2():
	adst.withdraw()
	root.deiconify()

def f3():
	stdata.delete(1.0, END)	#delete previous data from scrolled text
	root.withdraw()
	vist.deiconify()
	con = None
	cursor = None
	try:
		con = connect('system/abc123')
		cursor = con.cursor()
		sql = "select rno,name,marks from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ""
		for d in data:
			msg = msg + "rno = " + str(d[0]) + " name = " + str(d[1]) + "\n" + " marks = " + str(d[2]) + "\n"
		stdata.insert(INSERT, msg)
	except DatabaseError as e:
		print("Issue",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

def f4():
	vist.withdraw()
	root.deiconify()

def f5():
	con = None
	cursor = None
	try:	
		con = connect('system/abc123')
		rno = int(entAddRno.get())
		name = entAddName.get()
		marks = int(entAddMarks.get())
		
		if rno <= 0:
			messagebox.showerror("Error","Enter Positive Numbers")
			entAddRno.delete(0,END)
			entAddRno.focus()
		
		elif name.isalpha() ==	False:
			messagebox.showerror("Error","Enter Letters only")
			entAddName.delete(0,END)
			entAddName.focus()

		elif marks > 100 or marks < 0 :
			messagebox.showerror("Error","Enter Marks between 0 and 100 ")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
		else:
			cursor = con.cursor()
			sql = "insert into student values('%d','%s','%d')"
			args = (rno,name,marks)
			cursor.execute(sql % args)
			con.commit()	
			messagebox.showinfo("Success","record inserted")
			entAddRno.delete(0,END)
			entAddName.delete(0,END)
			entAddMarks.delete(0,END)
			entAddRno.focus()
	except DatabaseError as e:
		con.rollback()
		messagebox.showerror("Issue", "number already exist")
		entAddRno.delete(0,END)
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		entAddRno.focus()
	except ValueError as e:
		con.rollback()	
		messagebox.showerror("Warning!", "enter valid parameter")	
		entAddRno.delete(0,END)
		entAddMarks.delete(0,END)
		entAddName.delete(0,END)
		entAddRno.focus()
	
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()


def f6():
	root.withdraw()
	upst.deiconify()

def f7():
	upst.withdraw()
	root.deiconify()

def f8():
	root.withdraw()
	dst.deiconify()

def f9():
	dst.withdraw()
	root.deiconify()	

def f10():
	cursor = None
	con = None
	try:
		con = connect('System/abc123')
		rno = int(entUpdatedRno.get())
		name = entUpdatedName.get()
		marks = int(entUpdatedMarks.get())
		
		if rno <= 0 and rno.isdigit() == False:
			messagebox.showerror("Error","Enter Positive Numbers")
			entUpdatedRno.delete(0,END)
			entUpdatedRno.focus()
		
		elif name.isalpha() ==	False:
			messagebox.showerror("Error","Enter Letters only")
			entUpdatedRno.delete(0,END)
			entUpdatedRno.focus()

		elif marks > 100 or marks < 0 :
			messagebox.showerror("Error","Enter Marks between 0 and 100 ")
			entUpdatedMarks.delete(0,END)
			entUpdatedMarks.focus()
		else:
			cursor = con.cursor()
			sql = "update student set name = '%s',marks = '%d' where rno = '%d'"
			args = (name, marks, rno)
			cursor.execute(sql % args)
			con.commit()
			msg = str(cursor.rowcount)+"Record Updated"
			if cursor.rowcount == 0:
				messagebox.showerror("Error","Record does not exist")
			else:
				messagebox.showinfo("Success","record updated")
			entUpdatedRno.delete(0,END)
			entUpdatedName.delete(0,END)
			entUpdatedMarks.delete(0,END)
			entUpdatedRno.focus()
	except DatabaseError as e:
		con.rollback()
		print("Issue ", "Record does not found")
	except ValueError as e:
		messagebox.showerror("Warning!", "enter valid parameters")
		con.rollback()
		entUpdatedRno.delete(0,END)
		entUpdatedName.delete(0,END)
		entUpdatedMarks.delete(0,END)
		entUpdatedRno.focus()
	
	
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	

def f11():
	con = None
	Cursor = None
	try:
		con = connect('System/abc123')
		rno = int(entDeletedRno.get())
		cursor = con.cursor()
		sql = "delete from student where rno = '%d'"
		args = (rno)
		cursor.execute(sql % args)
		con.commit()
		if cursor.rowcount == 0:
			messagebox.showinfo("Error","record does not exist")
		else:
			msg = str(cursor.rowcount)+ "Record Deleted"
			messagebox.showinfo("Success","record deleted")
		entDeletedRno.delete(0,END)
		entDeletedRno.focus()
	except DatabaseError as e:
		con.rollback()
		print("Issue ", "Record Does Not Exist")
	except ValueError:
		messagebox.showerror("Error","Enter Numbers only")
		con.rollback()
	finally:
		if con is not None:
			con.close()

def g1():
	students=[]
	highest=[]
	marks=[]
	c={}
	con = connect('System/abc123')
	cursor = con.cursor()
	sql = "select name,marks from student"
	cursor.execute(sql)
	fetch = cursor.fetchall()
	for d in fetch:
		mar=int(d[1])
		marks.append(mar)
		stu=(d[0])
		students.append(stu)
	d=dict(zip(marks,students))
	lol=list(d.items())
	lol.sort()
	b = lol[-1:-4:-1]
	c.update(b)
	plt.bar(c.values(),c.keys(),color=['r','b','g'],width=0.2)
	plt.title("Top 3",fontsize=30)
	plt.ylabel("Marks",fontsize=15)
	plt.xlabel("Students",fontsize=15)
	plt.grid()
	plt.show()
	con.close()
	

btnAdd = Button(root,text="Add",font=('comic sans ms',16,'bold'), width = 10, command = f1)
btnView = Button(root,text="View",font=('comic sans ms',16,'bold'), width = 10, command = f3)
btnUpdate = Button(root,text="Update",font=('comic sans ms',16,'bold'), width = 10, command = f6)
btnDelete = Button(root,text="Delete",font=('comic sans ms',16,'bold'), width = 10, command = f8)
btnGraph = Button(root,text="Graph",font=('comic sans ms',16,'bold'), width = 10, command = g1)

entCity = Entry(root,font=("arial",13,"bold"),width=10)
entCity.insert(850,city)
lb1City = Label(root,text="City: ",font=("arial",13,"bold"))

entTemp=Entry(root,font=("arial",13,"bold"),width=10)
x=str(temp)+chr(176)+"C"
entTemp.insert(850,x)
lblTemp=Label(root,text="Temperature: ",font=("arial",13,"bold"))

entQuote=Entry(root,width=60,font=("arial",13,"bold"))
entQuote.insert(850, t1 )     
lblQuote=Label(root,text=" Quote of the day: ",font=("arial",13,"bold"))

btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnGraph.pack(pady = 10)

lb1City.place(x=20,y=380)
entCity.place(x=70,y=380)
lblQuote.place(x=200,y=420)
entQuote.place(x=20,y=446)
lblTemp.place(x=300,y=380)
entTemp.place(x=420,y=380)

# Add

adst = Toplevel(root)
adst.title("Add S")
adst.geometry("500x550+200+200")
adst.configure(background = "black")

lblAddRno = Label(adst,text="Enter roll no",font=('comic sans ms',16,'bold'))
entAddRno = Entry(adst,bd=5,font=('comic sans ms',16,'bold'))

lblAddName = Label(adst,text="Enter name",font=('comic sans ms',16,'bold'))
entAddName = Entry(adst,bd=5,font=('comic sans ms',16,'bold'))

lblAddMarks = Label(adst,text="Enter marks",font=('comic sans ms',16,'bold'))
entAddMarks = Entry(adst,bd=5,font=('comic sans ms',16,'bold'))

btnAddSave = Button(adst,text="Save",font=('comic sans ms',16,'bold'), width = 10, command = f5)
btnAddBack = Button(adst,text="Back",font=('comic sans ms',16,'bold'), width = 10, command = f2)
lblAddRno.pack(pady = 10)
entAddRno.pack(pady = 10)
lblAddName.pack(pady = 10)
entAddName.pack(pady = 10)
lblAddMarks.pack(pady = 10)
entAddMarks.pack(pady = 10)
btnAddSave.pack(pady = 10)
btnAddBack.pack(pady = 10)

adst.withdraw()

#View

vist = Toplevel(root)
vist.title("View S")
vist.geometry("500x500+200+200")
vist.configure(background = "black")

stdata = scrolledtext.ScrolledText(vist, width = 30, height = 22)
btnViewBack = Button(vist, text="Back",font=('comic sans ms',16,'bold'), width = 10, command = f4)

stdata.pack(pady = 10)
btnViewBack.pack(pady = 10)

vist.withdraw()


#Update

upst = Toplevel(root)
upst.title("Update S")
upst.geometry("500x550+200+200")
upst.configure(background = "black")

lb1UpdateRno = Label(upst,text="Enter roll no",font=('comic sans ms',16,'bold'))
entUpdatedRno = Entry(upst,bd=5,font=('comic sans ms',16,'bold'))

lb1UpdateName = Label(upst,text="Enter name",font=('comic sans ms',16,'bold'))
entUpdatedName = Entry(upst,bd=5,font=('comic sans ms',16,'bold'))

lb1UpdateMarks = Label(upst,text="Enter marks",font=('comic sans ms',16,'bold'))
entUpdatedMarks = Entry(upst,bd=5,font=('comic sans ms',16,'bold'))

btnUpdateSave = Button(upst,text="Save",font=('comic sans ms',16,'bold'), width = 10, command = f10)
btnUpdateBack = Button(upst,text="Back",font=('comic sans ms',16,'bold'), width = 10, command = f7)
lb1UpdateRno.pack(pady = 10)
entUpdatedRno.pack(pady = 10)
lb1UpdateName.pack(pady = 10)
entUpdatedName.pack(pady = 10)
lb1UpdateMarks.pack(pady = 10)
entUpdatedMarks.pack(pady = 10)
btnUpdateSave.pack(pady = 10)
btnUpdateBack.pack(pady = 10)

upst.withdraw()

#delete

dst = Toplevel(root)
dst.title("Delete S")
dst.geometry("500x300+100+100")
dst.configure(background = "black")

lb1DeleteRno = Label(dst,text="Enter roll no",font=('comic sans ms',16,'bold'))
entDeletedRno = Entry(dst,bd=5,font=('comic sans ms',16,'bold'))

btnDeleteSave = Button(dst,text="Save",font=('comic sans ms',16,'bold'), width = 10, command = f11)
btnDeleteBack = Button(dst,text="Back",font=('comic sans ms',16,'bold'), width = 10, command = f9)
lb1DeleteRno.pack(pady = 10)
entDeletedRno.pack(pady = 10)

btnDeleteSave.pack(pady = 10)
btnDeleteBack.pack(pady = 10)

dst.withdraw()

#graph

grap = Toplevel(root)
grap.title("GRAPH")
grap.geometry("500x300+200+200")
grap.configure(background = "black")

btngrapBack = Button(grap,text="Back",font=("arial",18,"bold"),width=10,command=f2)
btngrapBack.pack(pady=10)

grap.withdraw()

root.mainloop()