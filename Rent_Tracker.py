
from tkinter import *
import sqlite3 as db
from tkcalendar import DateEntry


def submit():
    # connect to a database
    conn = db.connect('expense.db')
    #Create cursor for db
    c = conn.cursor()

    # Insert into Table
    
    c.execute("INSERT INTO expenses VALUES (:date, :amount, :name, :paid_by)",
        {
            'date': date_entry.get_date(),
            'amount': amount_entry.get(),
            'name': name_entry.get(),
            'paid_by': paid_by_entry.get()
            
        }
    )

    conn.commit()
    conn.close()

    # Clearing the fields
    name_entry.delete(0, END)
    amount_entry.delete(0,END)
    paid_by_entry.delete(0,END)

    total_label.config(text = "Expense Total: $" + str(total_expenses()))

    # updating record display
    view_records()
    return

def view_records():
    # connect to a database
    conn = db.connect('expense.db')
    #Create cursor for db
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM expenses")
    records = c.fetchall()

    # Delete list before repopulating
    rec_list.delete(0, END)
    
    for rec in records:
        # print(rec)
        rec_list.insert(END, str(rec[4]) + "________________" + str(rec[0]) + "______________" + str(rec[1]) + "_____________________" + str(rec[2]) + "_____________" + str(rec[3]))
    
    # print("_______________________________________")
    # # for each in rec_list:
    # #     print(each)
    # for i, listbox_entry in enumerate(rec_list.get(0, END)):
    #     print(listbox_entry)

    rec_list.pack(side=LEFT, fill=None, expand=False)

    scrollbar.config(command = rec_list.yview)

    conn.commit()
    conn.close()
    return

"""
Calculates Total Expenses
"""
def total_expenses():
    # connect to a database
    conn = db.connect('expense.db')
    #Create cursor for db
    c = conn.cursor()

    # Query the database
    total_expense = 0
    for row in c.execute('SELECT * FROM expenses'):
        try:
            total_expense += float(row[1])
        except:
            pass
    # total_label.config(text = "Expense Total: $" + str(total_expense))
    conn.commit()
    conn.close()
    return round(total_expense,2)

"""
Delete Records
"""
def delete():
    # connect to a database
    conn = db.connect('expense.db')
    #Create cursor for db
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE FROM expenses WHERE oid=" + delete_entry.get())
    delete_entry.delete(0, END)

    conn.commit()
    conn.close()

    # refresh records
    view_records()
    return


"""Initializing Program"""
conn = db.connect("expense.db")
curr = conn.cursor()
query = '''
create table if not exists expenses (
    name string,
    amount number,
    paid_by string,
    date string
    )
'''
curr.execute(query)
conn.commit()


# Creating GUI
root = Tk()
root.title("Rent Tracker")
root.geometry('600x800')

# Creating Frames
f1 = Frame(root, width=600, height=300)
f1.pack()

f2 = Frame(root, width=600, height=300)
f2.pack(fill=None, expand=False)


# Initializing List of Records and Scrollbar
scrollbar = Scrollbar(f2)
scrollbar.pack(side=RIGHT, fill=Y)
rec_list = Listbox(f2, yscrollcommand = scrollbar.set)
rec_list.config(width=250, height=200)

# Creating Labels and Entries
date_label=Label(f1,text="Date")
date_label.grid(row=1,column=0,padx=7,pady=7)
date_entry=DateEntry(f1, width=30)
date_entry.grid(row=1,column=1,padx=7,pady=7)

amount_label = Label(f1, text = "Amount")
amount_label.grid(row=2, column=0, padx=7, pady=7)
amount_entry=Entry(f1, width=30)
amount_entry.grid(row=2,column=1,padx=7,pady=7)

name_label=Label(f1, text="Expense")
name_label.grid(row=3,column=0,padx=7,pady=7)
name_entry=Entry(f1, width=30)
name_entry.grid(row=3,column=1,padx=7,pady=7)

paid_by_label = Label(f1, text = "Paid By")
paid_by_label.grid(row=4, column=0, padx=7, pady=7)
paid_by_entry=Entry(f1, width=30)
paid_by_entry.grid(row=4,column=1,padx=7,pady=7)

# Submit Button
submit_btn = Button(f1, text="Submit Expense", command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

# Total Expenses
total_label = Label(f1, text = "Expense Total: $" + str(total_expenses()))
total_label.grid(row=6, column=0, columnspan=2)

# View Expenses
query_btn = Button(f1, text="Show Records", command=view_records)
query_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=105)
l=Label(f1,text="Date\t\t  Amount\t\t  Name\t\t  Paid By", justify=CENTER)
l.grid(row=11,column=0, columnspan= 2)


# Delete Records
delete_btn = Button(f1, text="Delete Record (Enter ID)", command=delete)
delete_btn.grid(row=8, column=0, padx=10, pady=20, ipadx=50)

delete_entry = Entry(f1, width=30)
delete_entry.grid(row=8,column=1)




root.mainloop()