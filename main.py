# import modules
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import os

# Feature idea: add personalized goals, like user can set a goal to save 3000 rupees.

# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions

# Function creates a file if it doesn't exist
# and sets the Initial amount


def readInitialAmount(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('5000')
            return '5000'
    else:
        with open(filename, 'r') as f:
            return f.readline()


# This function updates the Initial Amount in file passed as parameter
def updateInitialAmount(filename, new_first_line):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines[0] = str(new_first_line) + '\n'
    with open(filename, 'w') as f:
        for line in lines:
            f.write(line)


readInitialAmount("initialAmount")


def saveRecord():
    # Saves the current Record entered by user.
    if len(item_name.get()) == 0:
        return
    global data
    data.insertRecord(item_name=item_name.get(
    ), item_price=item_amt.get(), purchase_date=transaction_date.get())
    clearEntries()


def setDate():
    # Returns the Current date.
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')


def clearEntries():
    # Clears the entries in input boxes.
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')


def fetch_records():
    # Fetches all the records from database to show in UI.
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count,
                  values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)


def select_record(event):
    # Used to Select the specific record in UI
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def update_record():
    # Updates the Current Selected Record
    if len(item_name.get()) == 0:
        return
    global selected_rowid
    selected = tv.focus()
    # Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(),
                          dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(
            namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error',  ep)

        # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)


def spentAmount():
    # Returns the current total spent amount.
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    totalExpense = 0
    for i in f:
        for j in i:
            totalExpense = j
    return totalExpense


def totalBalance():
    # Shows the Total Expense and remaining balance.
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo(
                'Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {int(readInitialAmount('initialAmount')) - j}")


def refreshData():
    # Refreshes the data in UI upon any changes.
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()


def deleteRow():
    # Deletes the Selected Row
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()
    clearEntries()


def startMainWindow():
    # Starts the Main Window
    entry_window.withdraw()
    ws.deiconify()


def getMostExpensiveItem():
    # Returns the Most Expensive Item
    item = data.fetchRecord(
        query="SELECT item_name, item_price FROM expense_record WHERE item_price = (SELECT MAX(item_price) FROM expense_record);")
    return item


def pieData():
    # Fetches the data from database then uses it to show a pie chart.
    unusedAmount = int(readInitialAmount('initialAmount')) - spentAmount()
    labels = data.fetchRecord(query="select item_name from expense_record")
    labelArray = [element[0] for element in labels]
    labelData = data.fetchRecord(query="select item_price from expense_record")
    labelDataArray = [element[0] for element in labelData]
    labelArray.append('Unused Amount')
    labelDataArray.append(unusedAmount)
    plt.pie(labelDataArray, labels=labelArray)
    plt.show()


def onClosing():
    # Makes sure to close all the running processes on exit.
    ws.destroy()


def isDatabaseEmpty():
    # Returns true or false based on database is empty or not.
    flag = data.fetchRecord(query="select item_name from expense_record")
    if len(flag) != 0:
        return True
    return False


def backToMain():
    # Takes you to back to the main window.
    ws.withdraw()
    entry_window.deiconify()


def changeBalance():
    # Shows a dialog box to change the total balance.
    userInput = simpledialog.askinteger(title="Adjust Balance", prompt='Enter total money you currently have:           ')
    if userInput is not None:
        updateInitialAmount('initialAmount', userInput)
    else:
        userInput = readInitialAmount('initialAmount')
        updateInitialAmount('initialAmount', userInput)


# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
ws.geometry("720x400")
ws.minsize(720, 400)
ws.maxsize(720, 400)
ws.withdraw()


# Entry tkinter window
entry_window = tk.Toplevel()
entry_window.geometry("500x300")
entry_window.minsize(500, 300)
entry_window.maxsize(500, 300)
entry_window.protocol("WM_DELETE_WINDOW", onClosing)
entry_window.config(bg='#F5F5F5')


# variables
f = ('Open Sans', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()


# add elements to second window
label = tk.Label(entry_window, text="SpendWise", font=f, fg='#424242')
label.pack()

# Checking if database is empty or not, then showing the button/labels
if isDatabaseEmpty():
    spentLabel = tk.Label(
        entry_window, text=f'Your total Expense to date: Rs {spentAmount()}', font=f, fg="#424242")
    spentLabel.pack()
    mostExpensiveItem = tk.Label(
        entry_window, text=f'Your Most Expensive item was: {getMostExpensiveItem()[0][0]} Rs {getMostExpensiveItem()[0][1]}', font=f, fg='#424242')
    mostExpensiveItem.pack()
    pieChart = tk.Button(entry_window, text="Show Spendings Chart", font=f, bg="#80CBC4", borderwidth=0, fg='white', command=pieData,  highlightthickness=5, width=20)
    pieChart.pack(padx=10, pady=10)

button = tk.Button(entry_window, text="Start Adding Entries", font=f,
                   bg="#80CBC4", borderwidth=0, fg='white', command=startMainWindow, width=20)
button.pack()
adjustBalance = tk.Button(entry_window, text='Adjust Balance', font=f, bg="#80CBC4", borderwidth=0, fg='white', width=20, command=changeBalance)
adjustBalance.pack(padx=5, pady=10)

closeButton = tk.Button(entry_window, text="Close Window", font=f, command=lambda: ws.destroy(), bg='#80CBC4', fg='white', borderwidth=0, width=20)
closeButton.pack(pady=10, padx=10)


# Frame widget
f2 = Frame(ws)
f2.pack()

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1,
    text='Current Date',
    font=f,
    bg='#673AB7',
    command=setDate,
    width=15,
    borderwidth=0,
    fg='white'
)

submit_btn = Button(
    f1,
    text='Save Record',
    font=f,
    command=saveRecord,
    bg='#4CAF50',
    fg='white',
    borderwidth=0,
)

clr_btn = Button(
    f1,
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg='#FFC107',
    fg='white',
    borderwidth=0
)

quit_btn = Button(
    f1,
    text='Exit',
    font=f,
    command=lambda: ws.destroy(),
    bg='#9E9E9E',
    fg='white',
    borderwidth=0
)

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#2196F3',
    command=totalBalance,
    borderwidth=0,
    fg='white'
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda: data.fetchRecord('select sum(ite)'),
    borderwidth=0,
    fg='white'
)

update_btn = Button(
    f1,
    text='Update',
    bg='#B9770E',
    command=update_record,
    font=f,
    borderwidth=0,
    fg='white'
)

del_btn = Button(
    f1,
    text='Delete',
    bg='#F44336',
    command=deleteRow,
    font=f,
    borderwidth=0,
    fg='white'
)

goBack = Button(
    f1,
    text='Go Back',
    bg='#FF9800',
    font=f,
    borderwidth=0,
    fg='white',
    command=backToMain
)

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0), pady=6)
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
goBack.grid(row=3, column=2, sticky=EW, padx=(10, 0), pady=(10, 0), columnspan=2)

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("clam")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function
fetch_records()

# infinite loop
ws.mainloop()
