# Import necessary libraries and modules
import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import RandomForestRegressor
import numpy as np


class ExpenseTrackerApp:
    # Initialize the main application window and set up database connection
    def __init__(self):
        self.root = Tk()
        self.root.title('AI-Powered Expense Tracker')
        self.root.geometry('1200x600')
        self.root.resizable(0, 0)

        self.dataentery_frame_bg = 'Gray'
        self.buttons_frame_bg = 'LightBlue'
        self.hlb_btn_bg = 'LightBlue'

        self.lbl_font = ('Georgia', 13)
        self.entry_font = 'Times 13 bold'
        self.btn_font = ('Gill Sans MT', 13)

        self.desc = StringVar()
        self.amnt = DoubleVar()
        self.payee = StringVar()
        self.MoP = StringVar(value='Cash')
        self.category_var = StringVar(value='Food')
        self.categories = ['Food', 'Fuel', 'Stationery', 'Bills', 'EMIs', 'Entertainment', 'Other']

        self.connector = sqlite3.connect("Expense Tracker.db")
        self.cursor = self.connector.cursor()

        # Modify database schema to add 'Category' column if it doesn't exist
        try:
            self.connector.execute('ALTER TABLE ExpenseTracker ADD COLUMN Category TEXT')
        except:
            pass

        # Create the ExpenseTracker table if it doesn't exist
        self.connector.execute(
            'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT, Category TEXT)'
        )
        self.connector.commit()

        self.initialize_frames()  # Initialize the frames for UI
        self.root.mainloop()

    # Set up frames for the user interface
    def initialize_frames(self):
        self.data_entry_frame = Frame(self.root, bg=self.dataentery_frame_bg)
        self.data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)

        self.buttons_frame = Frame(self.root, bg=self.buttons_frame_bg)
        self.buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.25)

        self.tree_frame = Frame(self.root)
        self.tree_frame.place(relx=0.25, rely=0.31, relwidth=0.75, relheight=0.65)

        # Add labels and fields for entering data
        Label(self.data_entry_frame, text='Date (M/DD/YY) :', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=50)
        self.date = DateEntry(self.data_entry_frame, date=datetime.datetime.now().date(), font=self.entry_font)
        self.date.place(x=160, y=50)

        Label(self.data_entry_frame, text='Description           :', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=100)
        Entry(self.data_entry_frame, font=self.entry_font, width=31, textvariable=self.desc).place(x=10, y=130)

        Label(self.data_entry_frame, text='Amount\t             :', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=180)
        Entry(self.data_entry_frame, font=self.entry_font, width=14, textvariable=self.amnt).place(x=160, y=180)

        Label(self.data_entry_frame, text='Payee\t             :', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=230)
        Entry(self.data_entry_frame, font=self.entry_font, width=31, textvariable=self.payee).place(x=10, y=260)

        Label(self.data_entry_frame, text='Mode of Payment:', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=310)
        dd1 = OptionMenu(self.data_entry_frame, self.MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
        dd1.place(x=160, y=305)
        dd1.configure(width=10, font=self.entry_font)

        Label(self.data_entry_frame, text='Category              :', font=self.lbl_font, bg=self.dataentery_frame_bg).place(x=10, y=355)
        OptionMenu(self.data_entry_frame, self.category_var, *self.categories).place(x=160, y=355)

        # Add buttons for actions like adding an expense, clearing fields, etc.
        Button(self.data_entry_frame, text='Add expense', command=self.add_another_expense, font=self.btn_font, width=30, bg=self.hlb_btn_bg).place(x=10, y=395)
        Button(self.data_entry_frame, text='Convert to words before adding', font=self.btn_font, width=30, bg=self.hlb_btn_bg, command=self.expense_to_words_before_adding).place(x=10, y=450)

        # Button configurations for managing expenses (delete, view, edit, etc.)
        Button(self.buttons_frame, text='Delete Expense', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.remove_expense).place(x=30, y=5)
        Button(self.buttons_frame, text='Clear Fields in DataEntry Frame', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.clear_fields).place(x=335, y=5)
        Button(self.buttons_frame, text='Delete All Expenses', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.remove_all_expenses).place(x=640, y=5)
        Button(self.buttons_frame, text='View Selected Expense\'s Details', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.view_expense_details).place(x=30, y=65)
        Button(self.buttons_frame, text='Edit Selected Expense', command=self.edit_expense, font=self.btn_font, width=25, bg=self.hlb_btn_bg).place(x=335, y=65)
        Button(self.buttons_frame, text='Convert Expense to a sentence', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.selected_expense_to_words).place(x=640, y=65)

        # Add Category selector and analyze button
        Label(self.buttons_frame, text='Select Category:', font=self.lbl_font, bg=self.buttons_frame_bg).place(x=30, y=130)
        OptionMenu(self.buttons_frame, self.category_var, *self.categories).place(x=180, y=130)

        Button(self.buttons_frame, text='Show Graph & Predict', font=self.btn_font, width=25, bg=self.hlb_btn_bg, command=self.analyze_category).place(x=335, y=125)

        # Set up treeview (table) to display the expense data
        self.table = ttk.Treeview(self.tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment', 'Category'))
        X_Scroller = Scrollbar(self.table, orient=HORIZONTAL, command=self.table.xview)
        Y_Scroller = Scrollbar(self.table, orient=VERTICAL, command=self.table.yview)
        X_Scroller.pack(side=BOTTOM, fill=X)
        Y_Scroller.pack(side=RIGHT, fill=Y)
        self.table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

        # Set column headers and configure table layout
        for col in ['ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment', 'Category']:
            self.table.heading(col, text=col, anchor=CENTER)

        self.table.column('#0', width=0, stretch=NO)
        for i in range(7):
            self.table.column(f'#{i+1}', width=120, stretch=NO)

        self.table.place(relx=0, y=0, relheight=1, relwidth=1)
        self.list_all_expenses()  # Populate the table with all expenses

    # List all expenses in the table view
    def list_all_expenses(self):
        self.table.delete(*self.table.get_children())
        data = self.connector.execute('SELECT * FROM ExpenseTracker').fetchall()
        for values in data:
            self.table.insert('', END, values=values)

    # Add a new expense to the database
    def add_another_expense(self):
        if not self.date.get() or not self.payee.get() or not self.desc.get() or not self.amnt.get() or not self.MoP.get():
            mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
        elif self.amnt.get() <= 0:
            mb.showerror("Invalid Amount", "Amount should be greater than zero.")
        elif len(self.desc.get()) > 100 or self.desc.get().isdigit():
            mb.showerror("Invalid Description", "Description is too long or only numeric.")
        else:
            self.connector.execute(
                'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, Category) VALUES (?, ?, ?, ?, ?, ?)',
                (self.date.get_date(), self.payee.get(), self.desc.get(), self.amnt.get(), self.MoP.get(), self.category_var.get())
            )
            self.connector.commit()
            self.clear_fields()
            self.list_all_expenses()
            mb.showinfo('Expense added', 'The expense has been added to the database')

    # Clear input fields
    def clear_fields(self):
        self.desc.set('')
        self.payee.set('')
        self.amnt.set(0.0)
        self.MoP.set('Cash')
        self.category_var.set('Food')
        self.date.set_date(datetime.datetime.now().date())
        self.table.selection_remove(*self.table.selection())

    # Remove selected expense from the database
    def remove_expense(self):
        if not self.table.selection():
            mb.showerror('No record selected!', 'Please select a record to delete!')
            return
        values_selected = self.table.item(self.table.focus())['values']
        surety = mb.askyesno('Are you sure?', f'Delete the record of {values_selected[2]}?')
        if surety:
            self.connector.execute('DELETE FROM ExpenseTracker WHERE ID=?', (values_selected[0],))
            self.connector.commit()
            self.list_all_expenses()

    # Remove all expenses from the database
    def remove_all_expenses(self):
        if mb.askyesno('Are you sure?', 'Delete all expenses?', icon='warning'):
            self.connector.execute('DELETE FROM ExpenseTracker')
            self.connector.commit()
            self.clear_fields()
            self.list_all_expenses()

    # View details of a selected expense
    def view_expense_details(self):
        if not self.table.selection():
            mb.showerror('No expense selected', 'Please select an expense to view details')
            return
        values = self.table.item(self.table.focus())['values']
        self.date.set_date(datetime.date.fromisoformat(values[1]))
        self.payee.set(values[2])
        self.desc.set(values[3])
        self.amnt.set(values[4])
        self.MoP.set(values[5])
        self.category_var.set(values[6] if len(values) > 6 else 'Other')

    # Edit a selected expense
    def edit_expense(self):
        if not self.table.selection():
            mb.showerror('No expense selected!', 'Please select an expense to edit!')
            return

        def save_edited_expense():
            values = self.table.item(self.table.focus())['values']
            self.connector.execute(
                'UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ?, Category = ? WHERE ID = ?',
                (self.date.get_date(), self.payee.get(), self.desc.get(), self.amnt.get(), self.MoP.get(), self.category_var.get(), values[0])
            )
            self.connector.commit()
            self.clear_fields()
            self.list_all_expenses()
            mb.showinfo('Edited', 'Expense updated successfully')
            edit_btn.destroy()

        self.view_expense_details()
        edit_btn = Button(self.data_entry_frame, text='Save Edited Expense', font=self.btn_font, width=30, bg=self.hlb_btn_bg, command=save_edited_expense)
        edit_btn.place(x=10, y=500)

    # Convert selected expense to words
    def selected_expense_to_words(self):
        if not self.table.selection():
            mb.showerror('No expense selected!', 'Please select an expense to read')
            return
        values = self.table.item(self.table.focus())['values']
        message = f"You paid ₹{values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"
        mb.showinfo('Expense Summary', message)

    # Convert the current expense to words before adding it
    def expense_to_words_before_adding(self):
        if not self.date.get() or not self.desc.get() or not self.amnt.get() or not self.payee.get() or not self.MoP.get():
            mb.showerror('Incomplete data', 'Fill all fields first!')
            return
        message = f"You paid ₹{self.amnt.get()} to {self.payee.get()} for {self.desc.get()} on {self.date.get_date()} via {self.MoP.get()}"
        if mb.askyesno('Add this expense?', message):
            self.add_another_expense()

    # Analyze a category and predict future spending
    def analyze_category(self):
        category = self.category_var.get()
        df = pd.read_sql_query("SELECT ID, Date, Amount, Category FROM ExpenseTracker", self.connector)

        if df.empty or category not in df['Category'].values:
            mb.showinfo("No data", f"No data found for category: {category}")
            return

        df = df[df['Category'] == category]
        df['ID'] = df['ID'].astype(str)

        X = np.arange(len(df)).reshape(-1, 1)
        y = df['Amount'].values

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        prediction = model.predict([[len(df)]])  # Predict next month's spending

        avg = y.mean()
        last = y[-1]
        pred = prediction[0]

        # Plotting the graph of expenses and prediction
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.bar(df['ID'], y, color='skyblue', label='Actual')
        ax.bar('P', pred, color='orange', label='Predicted')

        ax.set_title(f"{category} Expenses Overview", fontsize=14)
        ax.set_ylabel("Amount (₹)")
        ax.set_xlabel("Transaction ID")
        ax.legend()

        # Show the prediction summary
        canvas = FigureCanvasTkAgg(fig, master=Toplevel(self.root))
        canvas.draw()
        canvas.get_tk_widget().pack()

        if pred > avg * 1.25:
            msg = f"Prediction: You might spend ₹{pred:.2f} next month. That's higher than your average of ₹{avg:.2f}."
        elif pred < avg * 0.75:
            msg = f"Prediction: Expected spending ₹{pred:.2f} is significantly lower than your average of ₹{avg:.2f}."
        else:
            msg = f"Prediction: Your expected spend is ₹{pred:.2f} which is around your usual average of ₹{avg:.2f}."

        if last > avg:
            msg += "\nLast month you spent more than usual."
        else:
            msg += "\nLast month you spent less than usual."

        mb.showinfo("Prediction Summary", msg)


if __name__ == "__main__":
    ExpenseTrackerApp()
