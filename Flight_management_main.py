'''This script is a Tkinter GUI application for flight management.
It uses a number of libraries: datetime, tkinter, tkinter.messagebox, ttk, tkcalendar and tktimepicker.
It creates a database named 'FlightManagement.db' and if it doesn't exist, creates a table 'Flight_MANAGEMENT' within it.
The database stores flight details of passengers, with columns: FLIGHT_ID, NAME, EMAIL, PHONE_NO, GENDER, DOB, DEPARTURE, ARRIVAL, DEPARTURE_TIME, ARRIVAL_TIME.
The script also creates a number of functions to handle the management of flight details.
It includes functions to handle the submission of flight details, displaying flight details, resetting input fields and resetting the tree view.
It also implements error handling for the inputs and a variety of messageboxes for the users to provide feedback'''

#importing necessary libraries and modules
import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry  # pip install tkcalendar
from tktimepicker import AnalogPicker, AnalogThemes
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('FlightManagement.db')
cursor = connector.cursor()

connector.execute("CREATE TABLE IF NOT EXISTS Flight_MANAGEMENT (FLIGHT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, DEPARTURE TEXT, ARRIVAL TEXT,DEPARTURE_TIME TEXT, ARRIVAL_TIME TEXT)")

# Creating the functions
def reset_fields():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, DEPARTURE_strvar, ARRIVAL_strvar,DEPARTURE_TIME_strvar, ARRIVAL_TIME_strvar

    for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'DEPARTURE_strvar','ARRIVAL_strvar','DEPARTURE_TIME_strvar','ARRIVAL_TIME_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())
    
def reset_form():
    global tree
    tree.delete(*tree.get_children())

    reset_fields()


def display_records():
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM Flight_MANAGEMENT ')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)


def add_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, DEPARTURE_strvar, ARRIVAL_strvar,DEPARTURE_TIME_strvar, ARRIVAL_TIME_strvar

    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    departure = DEPARTURE_strvar.get()
    arrival = ARRIVAL_strvar.get()
    departure_time = DEPARTURE_TIME_strvar.get()
    arrival_time = ARRIVAL_TIME_strvar.get()

    if not name or not email or not contact or not gender or not DOB or not departure or not arrival or not  departure_time  or not arrival_time:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute('INSERT INTO FLIGHT_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, DEPARTURE, ARRIVAL,DEPARTURE_TIME, ARRIVAL_TIME) VALUES (?,?,?,?,?,?,?,?,?)', (name, email, contact, gender, DOB, departure, arrival,departure_time,arrival_time))
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute('DELETE FROM Flight_MANAGEMENT WHERE FLIGHT_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        display_records()


def view_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, DEPARTURE_strvar, ARRIVAL_strvar,DEPARTURE_TIME_strvar, ARRIVAL_TIME_strvar

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

    name_strvar.set(selection[1]); email_strvar.set(selection[2])
    contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
    dob.set_date(date); DEPARTURE_strvar.set(selection[6]); ARRIVAL_strvar.set(selection[7])
    DEPARTURE_TIME_strvar.set(selection[8]);ARRIVAL_TIME_strvar.set(selection[9])


def del_db():
        connector.execute('delete from Flight_MANAGEMENT')
        connector.commit()

        mb.showinfo('Done', 'The database was successfully reset.')

        display_records()


# Initializing the GUI window
main = Tk()
main.title('Flight Management System')
main.geometry('1190x900')
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frame

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
DEPARTURE_strvar = StringVar()
ARRIVAL_strvar = StringVar()
DEPARTURE_TIME_strvar = StringVar()
ARRIVAL_TIME_strvar = StringVar()

# Placing the components in the main window
Label(main, text="FLIGHT MANAGEMENT SYSTEM", font=headlabelfont, bg='SpringGreen').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.03)
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.12)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.22)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.32)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.42)
Label(left_frame, text="Departure", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.52)
Label(left_frame, text="Arrival", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.61)
Label(left_frame, text="Departure Time", font=labelfont, bg=lf_bg).place(relx=0.18, rely=0.69)
Label(left_frame, text="Arrival Time", font=labelfont, bg=lf_bg).place(relx=0.24, rely=0.78)

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.08)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.17)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.27)
Entry(left_frame, width=19, textvariable=DEPARTURE_strvar , font=entryfont).place(x=20, rely=0.57)
Entry(left_frame, width=19, textvariable=ARRIVAL_strvar , font=entryfont).place(x=20, rely=0.65)
Entry(left_frame, width=19, textvariable=DEPARTURE_TIME_strvar , font=entryfont).place(x=20, rely=0.74)
Entry(left_frame, width=19, textvariable=ARRIVAL_TIME_strvar , font=entryfont).place(x=20, rely=0.83)

OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.37, relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.47)

Button(center_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.1, rely=0.85)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete database', font=labelfont, command=del_db, width=15).place(relx=0.1, rely=0.55)


# Placing components in the right frame
Label(right_frame, text='Flight Records', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Flight ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Departure","Arrival","Departure Time","Arrival Time"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Flight ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Departure', text='Departure', anchor=CENTER)
tree.heading('Arrival', text='Arrival', anchor=CENTER)
tree.heading('Departure Time', text='Departure Time', anchor=CENTER)
tree.heading('Arrival Time', text='Arrival Time', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.column('#8', width=150, stretch=NO)
tree.column('#9', width=150, stretch=NO)
tree.column('#10', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
