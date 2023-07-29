import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import date
import datetime
import time
from PIL import ImageTk,Image

# MySQL Connecting:

mydb=mysql.connector.connect(host='localhost',user='root',password='nehal292004!',database='Acadamix')
 


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  



#class details

def Class_details():
    clsdetwin = tk.Toplevel()
    clsdetwin.geometry('1366x768')
    clsdetwin.title('Acadamix - Create Class')
    clsdetwin.state('zoomed')

    clsdetwinpic = ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
    clsdetwinpanel = Label(clsdetwin, image=clsdetwinpic)
    clsdetwinpanel.pack(side='top', fill='both', expand='yes')
    
    def show():
        table_name = name.get()
        q = f"SELECT * FROM {table_name}"
        mycur = mydb.cursor()
        mycur.execute(q)
        result = mycur.fetchall()
        columns = [row[0] for row in mycur.description]

        columns_with_total = columns + ["Total"]

        ree = ttk.Treeview(clsdetwin, column=columns_with_total, show='headings', height=10)

        for col in columns_with_total:
            ree.heading(col, text=col)
            ree.column(col, width=80, minwidth=80, anchor=tk.CENTER)

        ree.place(x=700, y=100)

        for row in result:
        
            data_without_id = row[2:] 
            total = sum(data_without_id)
            row_with_total = row + (total,)
            ree.insert("", "end", values=row_with_total)

                    
            
    def search():
        table_name = name.get()
        q = f"SELECT * FROM {table_name} WHERE Id = %s"
        mycur = mydb.cursor()
        mycur.execute(q, (classid.get(),))
        result = mycur.fetchall()
        columns = [row[0] for row in mycur.description]

        columns_with_total = columns + ["Total"]

        ree = ttk.Treeview(clsdetwin, column=columns_with_total, show='headings', height=1)

        for col in columns_with_total:
            ree.heading(col, text=col)
            ree.column(col, width=80, minwidth=80, anchor=tk.CENTER)

        ree.place(x=700, y=500)

        for row in result:
            data_without_id = row[2:]  
            total = sum(data_without_id)
            row_with_total = row + (total,)

            ree.insert("", "end", values=row_with_total)

        
        
    Label(clsdetwin, text="Class Name:", width=20).place(x=200, y=200)

    name = Entry(clsdetwin)
    name.place(x=370, y=200)
    name.config(borderwidth=2, relief='sunken')
    
    Button(clsdetwin, text="SHOW", command=show).place(x=450, y=200)
    
    Label(clsdetwin, text="Student ID:", width=20).place(x=200, y=250)

    classid = Entry(clsdetwin)
    classid.place(x=370, y=250)
    classid.config(borderwidth=2, relief='sunken')
    
    Button(clsdetwin, text="SHOW", command=search).place(x=450, y=250)
    
    clsdetwin.mainloop()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# Login System:

def login():

    global username, password

    username=entry1.get()
    password=entry2.get()


    if (username == '' or password == ''):
            messagebox.showinfo('Error', 'Please fill the username and password')
    else:
        mcursor = mydb.cursor()
        query_check = "SELECT * FROM accounts WHERE USERNAME='{}' AND PASSWORD='{}'".format(username, password)
        mcursor.execute(query_check)
        existing_user = mcursor.fetchone()

        if existing_user:
            messagebox.showinfo('Logged in', 'Logged in successfully')
            logwin.destroy()
        else:
            messagebox.showinfo('Error', 'Incorrect Username or Password - Try Again')


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  

# create

def create_table():
    def check_and_create_table():
        class_name = classname.get()
        num_subjects = num_subjects_entry.get()
        num_subjects = int(num_subjects)
        
        if not class_name:
            messagebox.showerror('error','Enter class name')
        
        if num_subjects <= 0:
            messagebox.showerror('error','Enter correct number of subjects')

        create_table_in_db(class_name, num_subjects)

    def create_table_in_db(class_name, num_subjects):
        sql_query = f"CREATE TABLE {class_name} (Id varchar(20), Name char(20));"
        mycur = mydb.cursor()
        mycur.execute(sql_query)

        for i in range(num_subjects):
            subject_name = subject_listbox.get(i) 
            subject_table_query = f"ALTER TABLE {class_name} ADD COLUMN {subject_name} INTEGER;"
            mycur.execute(subject_table_query)
        
        if create_table_in_db:
            messagebox.showinfo('success','Class created')
            createwin.destroy()

        else:
            messagebox.showerror('error','Class not created')
            


        mydb.commit()

    createwin = tk.Toplevel()
    createwin.geometry('1366x768')
    createwin.title('Acadamix - Create Class')
    createwin.state('zoomed')

    createwinpic = ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
    createwinpanel = Label(createwin, image=createwinpic)
    createwinpanel.pack(side='top', fill='both', expand='yes')

    Label(createwin, text="Create Class", width=20).place(x=270, y=150)

    classname_label = Label(createwin, text="Class Name:", width=20)
    classname_label.place(x=200, y=200)

    classname = Entry(createwin)
    classname.place(x=370, y=200)
    classname.config(borderwidth=2, relief='sunken')

    num_subjects_label = Label(createwin, text="No. of Subjects:", width=20)
    num_subjects_label.place(x=200, y=250)

    num_subjects_entry = Entry(createwin)
    num_subjects_entry.place(x=370, y=250)
    num_subjects_entry.config(borderwidth=2, relief='sunken')

    subject_label = Label(createwin, text="Subject:", width=20)
    subject_label.place(x=200, y=300)

    subject_entry = Entry(createwin)
    subject_entry.place(x=370, y=300)
    subject_entry.config(borderwidth=2, relief='sunken')

    subject_listbox = Listbox(createwin, height=10, width=40)
    subject_listbox.place(x=200, y=350)

    def add_subject():
        subject = subject_entry.get()
        if subject:
            subject_listbox.insert(END, subject)
            subject_entry.delete(0, END)

    add_subject_button = Button(createwin, text="Add Subject", command=add_subject)
    add_subject_button.place(x=450, y=350)

    create_table_button = Button(createwin, text="Create Table", command=check_and_create_table)
    create_table_button.place(x=450, y=491)


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


    Label(createwin, text="Alter Class", width=20).place(x=1000, y=150)
    
    
    def Rename_class():
        qry = "alter table {} rename to {}".format(clas_old_entry.get(),clas_new_entry.get())
        mycur = mydb.cursor()
        mycur.execute(qry)
        mydb.commit()
        
        if Rename_class:
            messagebox.showinfo('success','Class renamed')
            createwin.destroy()
        
        else:
            messagebox.showerror('error','Class not renamed')
        
    Label(createwin, text="Rename Class to", width=20).place(x=800, y=200)
    clas_old_entry = Entry(createwin)
    clas_old_entry.place(x=1150, y=150)
    clas_old_entry.config(borderwidth=2, relief='sunken')

    clas_new_entry = Entry(createwin)
    clas_new_entry.place(x=1000, y=200)
    clas_new_entry.config(borderwidth=2, relief='sunken')
    
    create_table_button = Button(createwin, text="Rename class", command=Rename_class)
    create_table_button.place(x=1300, y=200)
    
    def Rename_sub():
        table_name = clas_old_entry.get()
        old_column_name = sub_old_entry.get()
        new_column_name = sub_new_entry.get()

        qry = "ALTER TABLE {} RENAME COLUMN {} TO {}".format(table_name, old_column_name, new_column_name)
        mycur = mydb.cursor()

        try:
            mycur.execute(qry)
            mydb.commit()
            messagebox.showinfo('Success', 'Subject renamed')
            createwin.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror('Error', 'Subject not renamed: {}'.format(err))

            
    
    Label(createwin, text="Rename Subject", width=20).place(x=800, y=300)
    sub_old_entry = Entry(createwin)
    sub_old_entry.place(x=1000, y=300)
    sub_old_entry.config(borderwidth=2, relief='sunken')
    Label(createwin, text="to", ).place(x=1130, y=300)
    sub_new_entry = Entry(createwin)
    sub_new_entry.place(x=1150, y=300)
    sub_new_entry.config(borderwidth=2, relief='sunken')
    
    create_tabl_button = Button(createwin, text="Rename Subject", command=Rename_sub)
    create_tabl_button.place(x=1300, y=300)
    
    def drop_sub():
        table_name = clas_old_entry.get()
        column_name = del_sub_entry.get()
        
        qry = "ALTER TABLE {} DROP COLUMN {}".format(table_name, column_name)
        mycur = mydb.cursor()

        try:
            mycur.execute(qry)
            mydb.commit()
            messagebox.showinfo('Success', 'Subject dropped')
            createwin.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror('Error', 'Subject not dropped: {}'.format(err))
        
    Label(createwin, text="Delete Subject", width=20).place(x=800, y=400)
    del_sub_entry = Entry(createwin)
    del_sub_entry.place(x=1000, y=400)
    del_sub_entry.config(borderwidth=2, relief='sunken')
    
    create_tabl_button = Button(createwin, text="Delete Subject", command=drop_sub)
    create_tabl_button.place(x=1300, y=400)
    
    createwin.mainloop()

      
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# update table

def update_table():
    
    upwin=tk.Toplevel()
    upwin.geometry('1366x768')
    upwin.title('Acadamix - Update class records')
    upwin.state('zoomed')
    upwinpic=ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
    upwinpanel=Label(upwin,image=upwinpic)
    upwinpanel.pack(side='top',fill='both',expand='yes')
    
    def ups():
        if old.get() == "name" or 'id':
            q="update {} set {} = '{}' where Id ='{}'".format(classname.get(),old.get(),new.get(),old1.get())
        else:
            q="update {} set {} = {} where Id ='{}'".format(classname.get(),old.get(),new.get(),old1.get())
        mycur = mydb.cursor()
        mycur.execute(q)
        mydb.commit()
        
        if ups:
            messagebox.showinfo('success',"A student record is updated")
            upwin.destroy()
        else: 
            messagebox.showerror('error',"Student record is not uppdated")

    def refer():
        table_name = classname.get()
        q = f"SELECT * FROM {table_name} WHERE Id = %s"
        mycur = mydb.cursor()
        mycur.execute(q, (old1.get(),))
        result = mycur.fetchall()

        columns = [row[0] for row in mycur.description]
        num_columns = len(columns)

        ree = ttk.Treeview(upwin, column=columns, show='headings', height=1)

        for col in columns:
            ree.heading(col, text=col)
            ree.column(col, width=80, minwidth=80, anchor=tk.CENTER)

        ree.place(x=700, y=100)

        for row in result:
            ree.insert("", "end", values=row)
    
    Label(upwin, text="Update Class", width=20).place(x=270, y=150)

    classname_label = Label(upwin, text="Class Name:", width=20)
    classname_label.place(x=200, y=200)

    classname = Entry(upwin)
    classname.place(x=370, y=200)
    classname.config(borderwidth=2, relief='sunken')
    
    refbutton = Button(upwin, text="Refer", command=refer)
    refbutton.place(x=560, y=200)

    subject_label = Label(upwin, text="Id", width=20)
    subject_label.place(x=200, y=250)
    
    old1 = Entry(upwin)
    old1.place(x=370, y=250)
    old1.config(borderwidth=2, relief='sunken')
    
    subject_label = Label(upwin, text="Col. to change", width=20)
    subject_label.place(x=200, y=300)
    
    old = Entry(upwin)
    old.place(x=370, y=300)
    old.config(borderwidth=2, relief='sunken')

    subject_label = Label(upwin, text="New Value", width=20)
    subject_label.place(x=200, y=350)

    new = Entry(upwin)
    new.place(x=370, y=350)
    new.config(borderwidth=2, relief='sunken')


    create_table_button = Button(upwin, text="Update", command=ups)
    create_table_button.place(x=450, y=500)
    
    upwin.mainloop()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# insert Page:

def insert_page():
    def insertcommands():
        
        def add_rec():
            subject = subj_entry.get()
            if subject:
                listbox.insert(tk.END, subject)
                subj_entry.delete(0, tk.END)
                
        def allin():
            tup = []
            for i in range(num_columns):
                rec_name = listbox.get(i)
                if i > 1:
                    rec_name = int(rec_name)
                else:
                    rec_name = str(rec_name)
                    
                tup.append(rec_name)
            tup = tuple(tup)
            query = f"INSERT INTO {cls.get()} VALUES {tup};"
            mycur.execute(query)

            mydb.commit()
            
            if allin:
                messagebox.showinfo('success',"A student record is added")
                insertwin.destroy()
            else: 
                messagebox.showerror('error',"Student record is not added")
            
            
        table_name = cls.get()
        q = f"DESC {table_name}"
        mycur = mydb.cursor()
        mycur.execute(q)
        result = mycur.fetchall()

        columns = [row[0] for row in result]
        num_columns = len(columns)

        ree = ttk.Treeview(insertwin, column=columns, show='headings', height=1)

        for col in columns:
            ree.heading(col, text=col)
            ree.column(col, width=80, minwidth=80, anchor=tk.CENTER)

        ree.place(x=500, y=100)

        listbox = Listbox(insertwin, height=10, width=40)
        listbox.place(x=200, y=300)

        Label(insertwin, text="Enter record : ", width=20).place(x=100, y=250)
        subj_entry = Entry(insertwin)
        subj_entry.place(x=250, y=250)

        add_subject_button = Button(insertwin, text="Add Record", command=add_rec)
        add_subject_button.place(x=500, y=300)
        
        button = Button(insertwin, text="Insert", command=allin)
        button.place(x=500, y=492)

        mydb.commit()

    insertwin = tk.Toplevel()
    insertwin.geometry('1366x768')
    insertwin.title('Acadamix - Insert records')
    insertwin.state('zoomed')

    insertwinpic = ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
    insertwinpanel = tk.Label(insertwin, image=insertwinpic)
    insertwinpanel.pack(side='top', fill='both', expand='yes')
    
    Label(insertwin, text="CLASS", width=20).place(x=100, y=100)
    cls = Entry(insertwin)
    cls.place(x=250, y=100)
    cls.config(borderwidth=2, relief='sunken')

    ok_button = Button(insertwin, text='OK', font=('Arial', 9), command=insertcommands, height=1, width=5,
                       bg='Lightsteelblue2', fg='gray6', activebackground='Skyblue', activeforeground='thistle1')
    ok_button.place(x=350, y=100)

    insertwin.mainloop()


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# About Page:

def aboutpage():

    about=tk.Toplevel()
    about.geometry('1366x768')
    about.title('Acadamix - About')
    about.state('zoomed')

    aboutpic=ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
    aboutpanel=Label(about,image=aboutpic)
    aboutpanel.pack(side='top',fill='both',expand='yes')

    def help():
        Label(about,text='''COSTUMER SERVICE NUMBER : +91 8438394310 (INDIA)
            MAIL ID                      : nehal292004@gmail.com''',font=('Arial',16)).place(x=750,y=550)

    Button(about,text='Contact Us',font=('Arial',20),command=help,height=1,width=16,bg='Lightsteelblue2',
    fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=800,y=500)

    Label(about,text=(""),font=('Arial',16),bg='pink').place(x=150,y=345)

    about.mainloop()
    

#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  



# Page Close Confirmations (Messagebox):

def homelogout():

    messagebox.showinfo('Thank You','Logged out successfully')
    home.destroy()

def logclose():

    if messagebox.askokcancel('Quit','Do you want to quit?'):
        logwin.destroy()
        quit()
        
def homeclose():

    if messagebox.askokcancel('Quit','Do you want to logout and quit?'):
        home.destroy()
        quit()



#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------  


# new user:

def newuser():
    username = entry1.get()
    query_check = "SELECT * FROM accounts WHERE USERNAME='{}'".format(username)
    mcursor = mydb.cursor()
    mcursor.execute(query_check)
    existing_user = mcursor.fetchone()

    if existing_user:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
    else:
        password = entry2.get()
        query_insert = "INSERT INTO accounts VALUES ('{}', '{}')".format(username, password)
        mcursor.execute(query_insert)
        mydb.commit()
        messagebox.showinfo("Success", "Account created successfully!")
     
     
     
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    
    
# Login Page:

logwin=tk.Tk()
logwin.title('Acadamix - LOGIN')
logwin.geometry('400x220')
logwin.resizable(False,False)
logwin.protocol('WM_DELETE_WINDOW',logclose)

logwinpic=ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix login.png"))
logwinpanel=Label(logwin,image=logwinpic)
logwinpanel.pack(side='top',fill='both',expand='yes')

Label(logwin,text='USERNAME :',bg='white',font=('Arial',12),borderwidth=1,relief='solid').place(x=40,y=25)
Label(logwin,text='PASSWORD :',bg='white',font=('Arial',12),borderwidth=1,relief='solid').place(x=40,y=55)

global entry1,entry2,entry3

entry1=Entry(logwin)
entry1.place(x=220,y=25)
entry1.config(borderwidth=2,relief='sunken')

entry2=Entry(logwin)
entry2.place(x=220,y=55)
entry2.config(borderwidth=2,relief='sunken')
entry2.config(show='*')


Button(logwin,text='Create',command=newuser,height=1,width=10).place(x=100,y=120)
Button(logwin,text='Login',command=login,height=1,width=10).place(x=220,y=120)

logwin.mainloop()


#-------------------------------------------------------------------------------------------------------------------------------------------------------  
#-------------------------------------------------------------------------------------------------------------------------------------------------------    


# Home Page:

home=tk.Tk()
home.geometry('1366x768')
home.title('Acadamix')
home.state('zoomed')
home.protocol('WM_DELETE_WINDOW',homeclose)

currtime=time.strftime('%H:%M')
currdate=date.today().strftime("%d/%m/%Y")

homepic=ImageTk.PhotoImage(Image.open("E:\\NK Programs\\Python\\python save\\Acadamix\\Acadamix main.jpg"))
homepanel=Label(home,image=homepic)
homepanel.pack(side='top',fill='both',expand='yes')

Label(home,text=('User Name'),font=('Arial',16),bg='Lightsteelblue2').place(x=900,y=50) 
Label(home,text=(username),font=('Arial',16),bg='Lightsteelblue2').place(x=1050,y=50) 
Label(home,text=('Logged in: '+currtime+', '+currdate),font=('Arial',16),bg='pink').place(x=1050,y=100)

Button(home,text='Students Details',font=('Arial',20),command=Class_details,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=270,y=320)
Button(home,text='Create / Edit Class',font=('Arial',20),command=create_table,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=650,y=320)
Button(home,text='Edit Students',font=('Arial',20),command=update_table,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=1030,y=320)
Button(home,text='Add Students',font=('Arial',20),command=insert_page,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=650,y=480)
Button(home,text='About Us',font=('Arial',20),command=aboutpage,height=1,width=16,bg='Lightsteelblue2',
       fg='gray6',activebackground='Skyblue',activeforeground='thistle1').place(x=1030,y=480)
Button(home,text='Logout',font=('Arial',20),command=homelogout,height=1,width=10,bg='pink').place(x=1100,rely=0.85)

home.mainloop()
