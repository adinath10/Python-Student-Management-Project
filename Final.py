#STUDENT MANAGEMENT SYSTEM by Sahil Mukesh Ambre 

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from cx_Oracle import *
import matplotlib.pyplot as plt
import numpy as np 
from unidecode import unidecode
import requests 
import socket 
import bs4
import re


root = Tk()
root.title("Main Page ")
root.iconbitmap('book.ico')
root.geometry("500x600+250+250")
root.configure(background = 'orchid2')

#quote city temperature *****************************************************************************************
#****************************************************************************************************************
res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
#print(res)
soup = bs4.BeautifulSoup(res.text, 'lxml')
quote = soup.find('img', {"class":"p-qotd"})
#print(quote)
msg = quote['alt']
#print(msg)


try:
	socket.create_connection(("www.google.com",80))
	#print("you are connected")
	res = requests.get("https://ipinfo.io")
	#print(res)
	data = res.json()
	#print(data)
	city = unidecode(data['city'])
	#print(city)

	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res1 = requests.get(api_address)
	print(res1)
	data = res1.json()
	#print(data)
	
	atemp = data['main']['temp']
	#print("city ",city,"temp ",atemp)	

except OSError as e:
	print("Check connection",e)



def f1():
	root.withdraw()
	adst.deiconify()
def f2():
	adst.withdraw()
	root.deiconify()
def f3():  #View
	stdata.delete(1.0,END)
	root.withdraw()
	vist.deiconify()
	
	con = None
	try:
		con = connect('system/abc123')
		cursor = con.cursor()
		#sql = "select rno,name,marks from student"
		sql = "select * from student order by rno"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg = ""
		for d in data:
			msg = msg + "Roll no = " + str(d[0]) + " " + "Name = " + str(d[1]) + " " + "Marks = " + str(d[2]) + "\n"
		stdata.insert(INSERT, msg)
	except DatabaseError as e:
		print("Issue",e)
	finally:
		if con is not None:
			con.close()
		
def f4():
	vist.withdraw()
	root.deiconify()
def f5():
	root.withdraw()
	upst.deiconify()
def f6():
	upst.withdraw()
	root.deiconify()
def f7():
	root.withdraw()
	dlst.deiconify()
def f8():
	dlst.withdraw()
	root.deiconify()

def clean_add_inputs():
	entAddRno.delete(0,END)
	entAddName.delete(0,END)
	entAddMarks.delete(0,END)
	entAddRno.focus()

def clean_update_inputs():
	entUpdateRno.delete(0,END)
	entUpdateName.delete(0,END)
	entUpdateMarks.delete(0,END)
	entUpdateRno.focus()



def f9():             #add student record
	regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
	regex2 = re.compile('[0-9]') 
	con = None
	try:
		#entAddRno.focus()  
		con = connect('system/abc123')
		rno = int(entAddRno.get())
		name = entAddName.get()
		marks = int(entAddMarks.get())
		if len(name) < 2:  
			messagebox.showerror("Issue", "Name cannot be less than 2 characters" )
			clean_add_inputs()
		elif regex.search(name) != None or regex2.search(name) != None:
			messagebox.showerror("Issue", "Name cannot include digits or special characters")
			clean_add_inputs()
		elif marks < 0 or marks > 100:
			messagebox.showerror("Issue", "Marks cannot be less than 0 or greater than 100")
			clean_add_inputs()
		elif rno == 0:
			messagebox.showerror("Issue","Roll Number cannot be zero")
			clean_add_inputs()
		else:
			cursor = con.cursor()
			sql = "insert into student values('%d','%s','%d')"
			args = (rno,name,marks)
			cursor.execute(sql % args)
			con.commit()
			messagebox.showinfo("Success","Record added")
			clean_add_inputs()
	except ValueError as i: #error 
		messagebox.showerror("Issue","Enter valid parameters")
	except TypeError as e:  #error 
		messagebox.showerror("Issue","Enter valid parameters")
	except DatabaseError as e:
		con.rollback() 
		entAddRno.delete(0,END)
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		entAddRno.focus()
		messagebox.showerror("Issue", "Roll no already exists")
	finally:
		if con is not None:
			con.close()	

def f10():            #update student record 
	regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
	regex2 = re.compile('[0-9]') 
	con = None
	try:
		con = connect('system/abc123')
		rno = int(entUpdateRno.get())
		name = entUpdateName.get()
		marks = int(entUpdateMarks.get())
		if  len(name) < 2:
			messagebox.showerror("Issue", "Name cannot be less than 2 characters" )
			clean_update_inputs()
		elif regex.search(name) != None or regex2.search(name) != None:
			messagebox.showerror("Issue", "Name cannot include digits or special characters")
			clean_update_inputs()
		elif marks < 0 or marks > 100:
			messagebox.showerror("Issue", "Marks cannot be less than 0 or greater than 100")
			clean_update_inputs()
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
				messagebox.showerror("Issue","Record dosent exist")
		clean_update_inputs()
			
	except DatabaseError as e:
		con.rollback()
		print("issue",e)
		clean_update_inputs()
	finally:
		if con is not None:
			con.close()

def f11():            #delete student record 
	con = None
	try:
		con = connect('system/abc123')
		cursor = con.cursor()
		rno  = int(entDeleteRno.get())
		sql = "select rno from student where rno = " +str(rno)  
		cursor.execute(sql)
		data = cursor.fetchall()
		if data:
			sql = "delete from student where rno = '%d'"
			args = (rno)
			cursor.execute(sql % args)
			con.commit()
			#print(cursor.rowcount," record deleted")
			messagebox.showinfo("Succes","Record Deleted")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
		else:
			messagebox.showerror("Issue","Record does not exist")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print("issue",e)
	finally:
		if con is not None:
			con.close() 

def f12():  
	'''
	root.withdraw()
	grap.deiconify()
	'''
	students = []
	highest = []
	marks = []
	c = {}

	con = connect('system/abc123')
	cursor = con.cursor()
	sql = "select name, marks from student"
	cursor.execute(sql)
	fetch = cursor.fetchall()
	for d in fetch:
			mar = float(d[1])
			marks.append(mar)
			stu = (d[0])
			students.append(stu)
	d = dict(zip(marks,students))
	lol = list(d.items())
	lol.sort()
	#print(lol)
	b = lol[-1:-6:-1]
	c.update(b)
	#print(c.values())
	#print(c.keys())
	plt.bar(c.values(),c.keys(), color = ['r','b','g','y','k'], width = 0.4)
	plt.title("Top 5", fontsize = 27)
	plt.ylabel("Marks", fontsize = 13)
	plt.xlabel("Names of Students", fontsize = 13)
	plt.grid()
	plt.show()
	con.close()

'''
def f13():
	grap.withdraw()
	root.deiconify()
'''


#MAIN PAGE *******************************************************
#*****************************************************************

btnAdd = Button(root, text = "Add", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f1)
btnView = Button(root, text = "View", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f3)
btnUpdate = Button(root, text = "Update", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f5)
btnDelete = Button(root, text = "Delete", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f7)
btnGraph = Button(root, text = "Graph", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f12)
lblCity = Label(root, text = "City:", font = ('arial',10,'italic'), width = 5)
lblTemp = Label(root, text = "Temperature:", font = ('arial',10,'italic'), width = 10)
lblQotd = Label(root, text = "Quote of the day:", font = ('arial',10,'italic'), width = 13)
lblCityName = Label(root, text = city, font = ('arial',10,'italic'), width = 10 )
lblCityTemp = Label(root, text = atemp, font = ('arial',10,'italic'), width = 5)
lblQotdDaily = Label(root, text = msg, font = ('arial',8,'italic','bold'))

btnAdd.place(x = 180, y = 20)
btnView.place(x = 180, y = 110)
btnUpdate.place(x = 180, y = 200)
btnDelete.place(x = 180, y = 290)
btnGraph.place(x = 180, y = 380)
lblCity.place(x = 40, y = 450)
lblTemp.place(x = 310, y = 450)
lblQotd.place(x = 40, y = 500)
lblCityName.place(x = 90, y =450)
lblCityTemp.place(x = 400, y = 450)
lblQotdDaily.place(x = 40, y = 540)

btnAdd.configure(bg = 'plum1')
btnView.configure(bg = 'plum1')
btnUpdate.configure(bg = 'plum1')
btnDelete.configure(bg = 'plum1')
btnGraph.configure(bg = 'plum1')

#ADD STUDENT **************************************************
#**************************************************************

def rnoandmarks(inp):
	if inp.isdigit():
		return True
		#print(inp)
	elif inp is "":
		return True
	else:
		return False
'''
def nameofstud(input):
	if input.isalpha():
		return True
	elif input is "":
		return True
	else:
		return True
'''

adst = Toplevel(root)
adst.title("Add student ")
adst.iconbitmap('book.ico')
adst.geometry("500x500+250+250")
adst.configure(background = 'DeepSkyBlue2')

lblAddEnterRno = Label(adst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20)
entAddRno = Entry(adst, bd = 5, font = ('arial',14,'italic'))
lblAddEnterName = Label(adst, text = "Enter Name", font = ('arial',14,'italic'), width = 15)
entAddName = Entry(adst, bd = 5, font = ('arial',14,'italic')) 
lblAddEnterMarks = Label(adst, text = "Enter marks ", font = ('arial',14,'italic'), width = 15)
entAddMarks = Entry(adst, bd = 5, font = ('arial',14,'italic'))
btnAddBack = Button(adst, text = "Back", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f2)
btnAddSave = Button(adst, text = "Save", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f9)

lblAddEnterRno.pack(pady = 10)
entAddRno.pack(pady = 10)
lblAddEnterName.pack(pady = 10)
entAddName.pack(pady = 10)
lblAddEnterMarks.pack(pady = 10)
entAddMarks.pack(pady = 10)
btnAddSave.pack(pady = 10)
btnAddBack.pack(pady = 10)

reg = adst.register(rnoandmarks)
entAddRno.config(validate = "key", validatecommand = (reg, '%P'))
entAddMarks.config(validate = "key", validatecommand = (reg, '%P'))


adst.withdraw()

#*****************************************************************
#VIEW STUDENT ****************************************************

vist = Toplevel(root)
vist.title("View student details")
vist.iconbitmap('book.ico')
vist.geometry("500x500+250+250")
vist.configure(background = 'DeepSkyBlue2')

stdata = scrolledtext.ScrolledText(vist, width = 40, height = 20)
btnViewBack = Button(vist, text="Back",font=('comic sans ms',16,'bold'), width = 10, command = f4)

stdata.pack(pady = 10)
btnViewBack.pack(pady = 10)

vist.withdraw()

#*****************************************************************
#UPADATE STUDENT ****************************************************

upst = Toplevel(root)
upst.title("Update Student ")
upst.iconbitmap('book.ico')
upst.geometry("500x500+250+250")
upst.configure(background = 'DeepSkyBlue2')

lblUpdateEnterRno = Label(upst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20)
entUpdateRno = Entry(upst, bd = 5, font = ('arial',14,'italic'))
lblUpdateEnterName = Label(upst, text = "Enter Name", font = ('arial',14,'italic'), width = 15)
entUpdateName = Entry(upst, bd = 5, font = ('arial',14,'italic')) 
lblUpdateEnterMarks = Label(upst, text = "Enter marks ", font = ('arial',14,'italic'), width = 15)
entUpdateMarks = Entry(upst, bd = 5, font = ('arial',14,'italic'))
btnUpdateBack = Button(upst, text = "Back", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f6)
btnUpdateSave = Button(upst, text = "Save", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f10)

lblUpdateEnterRno.pack(pady = 10)
entUpdateRno.pack(pady = 10)
lblUpdateEnterName.pack(pady = 10)
entUpdateName.pack(pady = 10)
lblUpdateEnterMarks.pack(pady = 10)
entUpdateMarks.pack(pady = 10)
btnUpdateSave.pack(pady = 10)
btnUpdateBack.pack(pady = 10)

regg = upst.register(rnoandmarks)
entUpdateRno.config(validate = "key", validatecommand = (regg, '%P'))
entUpdateMarks.config(validate = "key", validatecommand = (regg, '%P'))

upst.withdraw()

#DELETE STUDENT**************************************************
#****************************************************************

dlst = Toplevel(root)
dlst.title("Delete Student Record ")
dlst.iconbitmap('book.ico')
dlst.geometry("500x300+250+250")
dlst.configure(background = 'plum2')

lblDeleteEnterRno = Label(dlst, text = "Enter Roll Number", font = ('arial',14,'italic'),width = 20)
entDeleteRno = Entry(dlst, bd = 5, font = ('arial',14,'italic'))
btnDeleteBack = Button(dlst, text = "Back", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f8)
btnDeleteSave = Button(dlst, text = "Delete", font = ('comic sans ms',16,'bold'), width = 10, height = 1, command = f11)

lblDeleteEnterRno.pack(pady = 10)
entDeleteRno.pack(pady = 10)
btnDeleteSave.pack(pady = 10)
btnDeleteBack.pack(pady = 10)
btnDeleteBack.configure(bg = 'sky blue')
dlst.withdraw()

reg = dlst.register(rnoandmarks)
entDeleteRno.config(validate = "key", validatecommand = (reg, '%P'))


#GRAPH***********************************************************
#****************************************************************
'''
grap = Toplevel(root)
grap.title("Student graph ")
grap.iconbitmap('book.ico')
grap.geometry("250x250+250+250")
grap.configure(background = 'DeepSkyBlue2')


btnGraphBack = Button(grap, text = "Back", font = ('comic sans ms',16,'bold'), width = 10, height = 1)
btnGraphBack.pack(pady = 50)

grap.withdraw()
'''



root.mainloop()

#**************************************************************************
'''
assign commands to save buttons and refer function f5 from pr5 L12 for adding student record 
and create table student with name, rno, marks and drop previous table student 
'''
#**************************************************************************
 #create a functiont to delete all Records

 #rno should not be 0


 

















