#Author: Shantanu Kumar Rahut
#Purpose: To create a simple todo list

#import some modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

#assigning and initalizing some variables
root = tk.Tk()
root.title("Todo List")
root.geometry("400x250+500+300")

#connecting database
conn = sql.connect("todolist.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, task TEXT)") #primary id not needed here, but it is a good practice

#creating a listbox
taskList = []

#function to add task
def addTask():
    word = e1.get()
    if(len(word)==0):
        messagebox.showinfo("Error", "Please enter a task")
    else:
        taskList.append(word)
        cur.execute("INSERT INTO tasks(task) VALUES(?)", (word,))
        listUpdate()
        e1.delete(0, tk.END)

#function to update list
def listUpdate():
    clearList()
    for i in taskList:
        t.insert(tk.END, i)

#function to clear list
def clearList():
    t.delete(0, tk.END)


#function to delete one task
def deleteTask():
    try:
        val = t.get(t.curselection())
        if val in taskList:
            taskList.remove(val)
            listUpdate()
            cur.execute("DELETE FROM tasks WHERE task=?", (val,))
    except:
        messagebox.showinfo('Error', 'No Task Selected')


#function to delete all task
def deleteAll():
    if messagebox.askyesno("Delete All", "Are you sure you want to delete all tasks?"):
        while(len(taskList)!=0):
            taskList.pop()
        cur.execute("DELETE FROM tasks")
        listUpdate()

#function to exit the app
def quitApp():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

#function to retrieve database
def retrieveDB():
    while(len(taskList)!=0):
        taskList.pop()
    for row in cur.execute("SELECT task FROM tasks"):
        taskList.append(row[0])


#initializing lables and buttons
l1 = ttk.Label(root, text = 'To-Do List by Shantanu Kumar Rahut')
l2 = ttk.Label(root, text='Enter task title: ')
e1 = ttk.Entry(root, width=21)
t = tk.Listbox(root, width= 25, height=11, selectmode='SINGLE')
b1 = ttk.Button(root, text='Add task', width=20, command=addTask)
b2 = ttk.Button(root, text='Delete', width=20, command=deleteTask)
b3 = ttk.Button(root, text='Delete all', width=20, command=deleteAll)
b4 = ttk.Button(root, text='Exit', width=20, command=quitApp)

retrieveDB()
listUpdate()

#Place geometry
l2.place(x=50, y=50)
e1.place(x=50, y=80)
b1.place(x=50, y=110)
b2.place(x=50, y=140)
b3.place(x=50, y=170)
b4.place(x=50, y =200)
l1.place(x=50, y=10)
t.place(x=220, y = 50)
    
    
root.mainloop()

conn.commit()
cur.close()