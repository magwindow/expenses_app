import expenses_helper as eh
import sqlite3
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry, Calendar

window = tk.Tk()
window.title("My App")

frame_add_form = tk.Frame(window, bg="green")
frame_statistic = tk.Frame(window, bg="yellow")
frame_list = tk.Frame(window, bg="blue")

frame_add_form.grid(row=0, column=0, sticky="ns")
frame_statistic.grid(row=0, column=1)
frame_list.grid(row=1, column=0, columnspan=2, sticky="we")

items = eh.get_all_expenses_items()


def form_submit():
    amount = float(f_amount.get())
    payment_date = eh.get_timestamp_from_string(f_date.get())
    expense_id = items['accordance'][f_choose.get()]
    insert_payment = (amount, payment_date, expense_id)
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        query = """INSERT INTO payments(amount, payment_date, expense_id) VALUES (?,?,?);"""
        cursor.execute(query, insert_payment)
        db.commit()


l_choose = ttk.Label(frame_add_form, text="Choose an expense item")
f_choose = ttk.Combobox(frame_add_form, values=items['names'])
l_amount = ttk.Label(frame_add_form, text="Enter amount")
f_amount = ttk.Entry(frame_add_form, justify=tk.RIGHT)
l_date = ttk.Label(frame_add_form, text="Enter date")
f_date = DateEntry(frame_add_form, foreground="black", normalforeground="black",
                   selectforeground="white", background="white", date_pattern="dd-mm-YYYY")
btn_submit = ttk.Button(frame_add_form, text="Submit", command=form_submit)

l_choose.grid(row=0, column=0, sticky="w", padx=10, pady=10)
f_choose.grid(row=0, column=1, sticky="e", padx=10, pady=10)
l_amount.grid(row=1, column=0, sticky="w", padx=10, pady=10)
f_amount.grid(row=1, column=1, sticky="e", padx=10, pady=10)
l_date.grid(row=2, column=0, sticky="w", padx=10, pady=10)
f_date.grid(row=2, column=1, sticky="e", padx=10, pady=10)
btn_submit.grid(row=3, column=0, columnspan=2, sticky="n", padx=10, pady=10)

l_most_commot_text = tk.Label(frame_statistic, text="The most common item")
l_most_commot_value = tk.Label(frame_statistic, text=eh.get_most_common_item(), font="Helvetica 14 bold")
l_exp_item_text = tk.Label(frame_statistic, text="The most expensive item")
l_exp_item_value = tk.Label(frame_statistic, text=eh.get_most_exp_item(), font="Helvetica 14 bold")
l_exp_day_text = tk.Label(frame_statistic, text="The most expensive day")
l_exp_day_value = tk.Label(frame_statistic, text=eh.get_most_exp_day(), font="Helvetica 14 bold")
l_exp_month_text = tk.Label(frame_statistic, text="The most expensive month")
l_exp_month_value = tk.Label(frame_statistic, text=eh.get_most_exp_month(), font="Helvetica 14 bold")

l_most_commot_text.grid(row="0", column="0", sticky="w", padx=10, pady=10)
l_most_commot_value.grid(row="0", column="1", sticky="e", padx=10, pady=10)
l_exp_item_text.grid(row="1", column="0", sticky="w", padx=10, pady=10)
l_exp_item_value.grid(row="1", column="1", sticky="e", padx=10, pady=10)
l_exp_day_text.grid(row="2", column="0", sticky="w", padx=10, pady=10)
l_exp_day_value.grid(row="2", column="1", sticky="e", padx=10, pady=10)
l_exp_month_text.grid(row="3", column="0", sticky="w", padx=10, pady=10)
l_exp_month_value.grid(row="3", column="1", sticky="e", padx=10, pady=10)

# l_temp_frame_add_form = tk.Label(frame_add_form, text="frame_add_form")
# l_temp_frame_add_form.pack(expand=True, padx=20, pady=20)

heads = ("id", "name", "amount", "date")
table = ttk.Treeview(frame_list, show="headings")
table['columns'] = heads

for header in heads:
    table.heading(header, text=header, anchor="center")
    table.column(header, anchor="center")

for row in eh.get_table_data():
    table.insert('', tk.END, values=row)

scroll_pane = ttk.Scrollbar(frame_list, command=table.yview)
table.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
table.pack(expand=tk.YES, fill=tk.BOTH)

window.mainloop()
