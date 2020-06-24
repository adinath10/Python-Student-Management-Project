
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from cx_Oracle import *
import matplotlib.pyplot as plt
import numpy as np
import socket
import requests
import bs4
import re

root=Tk()
root.title("Student Record System")
#root.iconbitmap('book.ico')
root.geometry("800x800+300+100")
root.configure(background='blue')

#quote city temperature *****************************************************************************************
#****************************************************************************************************************
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup = bs4.BeautifulSoup(res.text, 'lxml')
quote = soup.find('img', {"class":"p-qotd"})
msg = quote['alt']
first=msg[0:31]
second=msg[31:70]

try:
	socket.create_connection(("www.google.com",80))
	res = requests.get("https://ipinfo.io")
	data = res.json()
	city = data['city']

	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res1 = requests.get(api_address)
	data = res1.json()
		
	atemp = data['main']['temp']
	
except OSError as e:
	print("Check connection",e)

#Add data***************************************************************
#***********************************************************************
def open_add_window():
	root.withdraw()
	adst.deiconify()

def close_add_window():
	adst.withdraw()
	root.deiconify()

def add_data():
	reg1 = re.compile('[0-9]')
	reg2 = re.compile('[!@~#$%^&*()-_+={}\/><|]')
	reg3 = re.compile('[a-zA-Z]')	
	con=None
	try:
		con=connect('system/abc123')
		rno=int(entAddRno.get())
		name=entAddName.get()
		marks=int(entAddMarks.get())
		if rno < 0:
			con.rollback()
			messagebox.showerror("Issue", "Rno cannot be negative")
			entAddRno.delete(0,END)
			entAddRno.focus()
		elif len(name) < 2:
			con.rollback()
			messagebox.showerror("Issue", "Name should contain less than 2 characters")
			entAddName.delete(0,END)
			entAddName.focus()
		elif reg1.search(name) != None or reg2.search(name) != None:
			con.rollback()
			messagebox.showerror("Issue", "Name should not contain any digits or special characters")
			entAddName.delete(0,END)
			entAddName.focus()	
		elif marks < 0:
			con.rollback()
			messagebox.showerror("Issue", "Marks cannot be less than zero")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
		elif marks > 100:
			con.rollback()
			messagebox.showerror("Issue","Marks cannot be more than 100")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
		else:
			cursor=con.cursor()
			sql= "insert into student values('%d','%s','%f')"
			args=(rno,name,marks)
			cursor.execute(sql%args)
			con.commit()
			messagebox.showinfo("Success","Record inserted")
			entAddRno.delete(0,END)
			entAddName.delete(0,END)
			entAddMarks.delete(0,END)
			entAddRno.focus()
	
	except DatabaseError:
		con.rollback()
		messagebox.showerror("Issue","Roll no. already exists")
	
	except ValueError as e:
		try:
			if reg2.search(str(rno)) != None or reg3.search(str(rno)) != None:
				con.rollback()
				messagebox.showerror("Issue", "Please check the parameters of Marks")
				entAddMarks.delete(0,END)
				entAddMarks.focus()	
			else:	
				con.rollback()
				messagebox.showerror("Issue",e)
				
		except UnboundLocalError:
			con.rollback()
			messagebox.showerror("Issue","Please check the parameters of Roll no. ")
			entAddRno.delete(0,END)
			entAddRno.focus()
	finally:
		if con is not None:
			con.close()

#View data*******************************************************************************
#****************************************************************************************
def view_data():
	stdata.delete(1.0,END)
	root.withdraw()
	view.deiconify()
	con=None
	try:
		con=connect('system/abc123')
		cursor=con.cursor()
		sql="select rno,name,marks from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		msg=""
		for d in data:
			msg=msg+"\nRoll no= " + str(d[0])+ " " + "Name= " +str(d[1]) + " " + "Marks= " + str(d[2])
		stdata.insert(INSERT,msg)
	except DatabaseError as e:
		print("Issue",e)
	finally:
		if con is not None:
			con.close()
def close_view_window():
	view.withdraw()
	root.deiconify()
	
#Update data************************************************************************************
#***********************************************************************************************
def update_data():
	reg1 = re.compile('[0-9]')
	reg2 = re.compile('[!@~#$%^&*()-_+={}\/><|]')
	reg3 = re.compile('[a-zA-Z]')
	con=None
	try:
		con=connect('system/abc123')
		rno=int(entUpRno.get())
		name=entUpName.get()
		marks=float(entUpMarks.get())
		
		if rno < 0:
			con.rollback()
			messagebox.showerror("Issue", "Rno cannot be negative")
			entUpRno.delete(0,END)
			entUpRno.focus()
		elif len(name) < 2:
			con.rollback()
			messagebox.showerror("Issue", "Name should contain less than 2 characters")
			entUpName.delete(0,END)
			entUpName.focus()
		elif reg1.search(name) != None or reg2.search(name) != None:
			con.rollback()
			messagebox.showerror("Issue", "Name should not contain any digits or special characters")
			entUpName.delete(0,END)
			entUpName.focus()	
		elif marks < 0:
			con.rollback()
			messagebox.showerror("Issue", "Marks cannot be less than zero")
			entUpMarks.delete(0,END)
			entUpMarks.focus()
		elif marks > 100:
			con.rollback()
			messagebox.showerror("Issue","Marks cannot be more than 100")
			entUpMarks.delete(0,END)
			entUpMarks.focus()
		else:
			cursor = con.cursor()
			sql = "select rno from student where rno = " +str(rno) 
			cursor.execute(sql)
			data = cursor.fetchall()
			if data:
				sql = "update student set name = '%s', marks = '%d' where rno = '%d'"
				args = (name,marks,rno)
				cursor.execute(sql % args)
				con.commit()
				messagebox.showinfo("Success","Record updated")
			else:
				con.rollback()
				messagebox.showerror("Issue","Record dosent exist")
				

	except DatabaseError as e:
		con.rollback()
		messagebox.showerror("issue",e)
		

	except ValueError as e:
		try:
			if reg2.search(str(rno)) != None or reg3.search(str(rno)) != None:
				con.rollback()
				messagebox.showerror("Issue", "Please check the parameters of marks")
				entUpMarks.delete(0,END)
				entUpMarks.focus()	
			else:	
				con.rollback()
				messagebox.showerror("Issue",e)
				
		except UnboundLocalError:
			con.rollback()
			messagebox.showerror("Issue","Please check the parameters of roll no.")
			entUpRno.delete(0,END)
			entUpRno.focus()
	
	finally:
		if con is not None:
			con.close()
		
def close_update_window():
	update.withdraw()
	root.deiconify()
def open_update_window():
	root.withdraw()
	update.deiconify()

#Delete data****************************************************************************
#***************************************************************************************
def open_delete_window():
	root.withdraw()
	delete.deiconify()
def close_delete_window():
	delete.withdraw()
	root.deiconify()
def delete_data():
	con=None
	try:
		con=connect('system/abc123')
		rno=int(entDelRno.get())
		sql = "select rno from student where rno = " +str(rno)  
		cursor.execute(sql)
		data = cursor.fetchall()
		if data:
			sql= "delete from student where rno='%d'"
			args=(rno)
			cursor.execute(sql%args)
			con.commit()
			messagebox.showinfo("Success","Record Deleted")
			entDelRno.delete(0,END)
			entDelRno.focus()
		else:
			messagebox.showerror("Issue","Record does not exist")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
	except ValueError :
		con.rollback()
		messagebox.showerror("issue","Enter valid parameters")
	except DatabaseError as e:
		con.rollback()
		messagebox.showerror("issue",e)
	finally:
		if con is not None:
			con.close()
#Graph of the data******************************************************************************
#***********************************************************************************************
def show_graph():
	students=[]
	highest=[]
	marks=[]
	c={}
	con=connect('system/abc123')
	cursor=con.cursor()
	sql="select name,marks from student"
	cursor.execute(sql)
	fetch=cursor.fetchall()
	for d in fetch:
		mar=float(d[1])
		marks.append(mar)
		stu=(d[0])
		students.append(stu)
	d=dict(zip(marks,students))
	lol=list(d.items())
	lol.sort()
	print(lol)
	b=lol[-1:-4:-1]
	c.update(b)
	print(c.values())
	print(c.keys())
	plt.bar(c.values(),c.keys(),color=['r','b','g'],width=0.2)
	plt.title("Toppers",fontsize=30)
	plt.ylabel("Marks",fontsize=15)
	plt.xlabel("Students",fontsize=15)
	plt.grid()
	plt.show()
	con.close()

#Buttons of root pg*******************************************************************
#*************************************************************************************	
btnAdd=Button(root,text="ADD Record",font=('comic sans ms',16,'bold'),width=15,command=open_add_window)
btnView=Button(root,text="VIEW Record",font=('comic sans ms',16,'bold'),width=15,command=view_data)
btnUpdate=Button(root,text="UPDATE Record",font=('comic sans ms',16,'bold'),width=15,command=open_update_window)
btnDelete=Button(root,text="DELETE Record",font=('comic sans ms',16,'bold'),width=15,command=open_delete_window)
btnGraph=Button(root,text="GRAPH",font=('comic sans ms',16,'bold'),width=15,command=show_graph)
btnBack=Button(root,text="Back",font=('comic sans ms',16,'bold'),width=15,command=root.destroy)

#Label city**************************************************************
#************************************************************************
lblcity=Label(root,text="City:",font=('comic sans ms',16,'bold'),bg='blue')
showcity=Label(root,text=city,bd=5,font=('comic sans ms',16,'bold'),bg='blue')

#Label temperature*******************************************************
#************************************************************************
lbltemp=Label(root,text="Temperature:",font=('comic sans ms',16,'bold'),bg='blue')
showtemp=Label(root,text=atemp,bd=5,font=('comic sans ms',16,'bold'),bg='blue')

#Label Quote************************************************************
#************************************************************************
lblQuote=Label(root,text="******Quote of the day******",font=('comic sans ms',16,'bold'),bg='blue')
showQuotef=Label(root,text=first,font=('comic sans ms',16,'bold'),bg='blue')
showQuotes=Label(root,text=second,font=('comic sans ms',16,'bold'),bg='blue')

#Display buttons**********************************************************
#*************************************************************************
btnAdd.place(x=300,y=10)
btnView.place(x=300,y=70)
btnUpdate.place(x=300,y=140)
btnDelete.place(x=300,y=210)
btnGraph.place(x=300,y=280)
btnBack.place(x=300,y=350)

lblcity.place(x=10,y=420)
showcity.place(x=80,y=420)
lbltemp.place(x=580,y=420)
showtemp.place(x=720,y=420)
lblQuote.place(x=250,y=480)
showQuotef.place(x=250,y=510)
showQuotes.place(x=250,y=540)

#Add data pg******************************************************************
#*****************************************************************************
adst=Toplevel(root)
#adst.iconbitmap('book.ico')
adst.title("Add Student Record")
adst.geometry("600x600+300+100")
adst.configure(background='blue')
lblAddRno=Label(adst,text="Enter rno",font=('comic sans ms',16,'bold'))
entAddRno=Entry(adst,bd=5,font=('comic sans ms',16,'bold'))
lblAddName=Label(adst,text="Enter name",font=('comic sans ms',16,'bold'))	
entAddName=Entry(adst,bd=5,font=('comic sans ms',16,'bold'))
lblAddMarks=Label(adst,text="Enter Marks",font=('comic sans ms',16,'bold'))	
entAddMarks=Entry(adst,bd=5,font=('comic sans ms',16,'bold'))
btnAddSave= Button(adst,text="Save",font=('comic sans ms',16,'bold'),command=add_data)
btnAddBack= Button(adst,text="Back",font=('comic sans ms',16,'bold'),command=close_add_window)

lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)
adst.withdraw()

#View pg**************************************************************************
#*********************************************************************************
view= Toplevel(root)
view.title("Display Student Record")
#view.iconbitmap('book.ico')
view.geometry("600x600+300+100")
view.configure(background='blue')

stdata=scrolledtext.ScrolledText(view,width=50,height=30)
btnViewBack=Button(view,text="Back",font=('comic sans ms',16,'bold'),command=close_view_window)
stdata.pack(pady=10)
btnViewBack.pack(pady=10)
view.withdraw()

#Udate pg***************************************************************************
#***********************************************************************************
update=Toplevel(root)
update.title("Update Student Record")
#update.iconbitmap('book.ico')
update.geometry("600x600+300+100")
update.configure(background='blue')

lblUpRno=Label(update,text="Enter roll no.",font=('comic sans ms',16,'bold'))
entUpRno=Entry(update,bd=5,font=('comic sans ms',16,'bold'))
lblUpName=Label(update,text="Enter new name",font=('comic sans ms',16,'bold'))
entUpName=Entry(update,bd=5,font=('comic sans ms',16,'bold'))
lblUpMarks=Label(update,text="Enter Marks",font=('comic sans ms',16,'bold'))
entUpMarks=Entry(update,bd=5,font=('comic sans ms',16,'bold'))
btnUpUpdate= Button(update,text="Update",font=('comic sans ms',16,'bold'),command=update_data)
btnUpBack= Button(update,text="Back",font=('comic sans ms',16,'bold'),command=close_update_window)

lblUpRno.pack(pady=10)
entUpRno.pack(pady=10)
lblUpName.pack(pady=10)
entUpName.pack(pady=10)
lblUpMarks.pack(pady=10)
entUpMarks.pack(pady=10)
btnUpUpdate.pack(pady=10)
btnUpBack.pack(pady=10)
update.withdraw()

#Delete data pg******************************************************************
#********************************************************************************
delete=Toplevel(root)
delete.title("Delete Student Record")
#delete.iconbitmap('book.ico')
delete.geometry("600x600+300+100")
delete.configure(background='blue')

lblDelRno=Label(delete,text="Enter roll no ",font=('comic sans ms',16,'bold'))
entDelRno=Entry(delete,bd=5,font=('comic sans ms',16,'bold'))
btnDelDelete=Button(delete,text="Delete",font=('comic sans ms',16,'bold'),command=delete_data)
btnDelBack=Button(delete,text="Back",font=('comic sans ms',16,'bold'),command=close_delete_window)
lblDelRno.pack(pady=10)
entDelRno.pack(pady=10)
btnDelDelete.pack(pady=10)
btnDelBack.pack(pady=10)
delete.withdraw()

#Graph pg************************************************************************
#********************************************************************************
graph=Toplevel(root)
graph.geometry("600x600+300+100")
#graph.iconbitmap('book.ico')
graph.title("Graphical Representation of Records")
graph.configure(background='blue')
graph.withdraw()

root.mainloop()

