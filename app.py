import expenses_helper as eh
import tkinter as tk
from tkinter import ttk

from tkcalendar import DateEntry


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.style = ttk.Style()
        self.style.configure("ErrLbl.TLabel", foreground="red", padding=(10, 10, 60, 10))
        self.style.configure("SmplLbl.TLabel", padding=(10, 10, 60, 10))
        self.style.configure("BldLbl.TLabel", font=("Helvetica", 14, "bold"), padding=(0, 10, 0, 10))
        self['background'] = "#EBEBEB"
        self.put_frames()

    def put_frames(self):
        self.add_form_frame = AddForm(self).grid(row=0, column=0, sticky="nswe")
        self.stat_frame = StatFrame(self).grid(row=0, column=1, sticky="nswe")
        self.table_frame = TableFrame(self).grid(row=1, column=0, columnspan=2, sticky="nswe")

    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()


class AddForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.items = eh.get_all_expenses_items()
        self.put_widgets()

    def put_widgets(self):
        self.l_choose = ttk.Label(self, text="Choose an expense item", style="SmplLbl.TLabel")
        self.f_choose = ttk.Combobox(self, values=self.items['names'])
        self.l_amount = ttk.Label(self, text="Enter amount")
        self.f_amount = ttk.Entry(self, justify=tk.RIGHT, validate="key",
                                  validatecommand=(self.register(self.validate_amount), '%P'))
        self.l_date = ttk.Label(self, text="Enter date")
        self.f_date = DateEntry(self, foreground="black", normalforeground="black",
                                selectforeground="white", background="white", date_pattern="dd-mm-YYYY")
        self.btn_submit = ttk.Button(self, text="Submit", command=self.form_submit)

        self.l_choose.grid(row=0, column=0, sticky="w", padx=10)
        self.f_choose.grid(row=0, column=1, sticky="e", padx=10)
        self.l_amount.grid(row=1, column=0, sticky="w", padx=10)
        self.f_amount.grid(row=1, column=1, sticky="e", padx=10)
        self.l_date.grid(row=2, column=0, sticky="w", padx=10)
        self.f_date.grid(row=2, column=1, sticky="e", padx=10)
        self.btn_submit.grid(row=3, column=0, columnspan=2, sticky="n", padx=10)

        self.f_date._top_cal.overrideredirect(False)

    def validate_amount(self, input):
        try:
            x = float(input)
            return True
        except ValueError:
            self.bell()
            return False

    def form_submit(self):
        flag = True

        payment_date = eh.get_timestamp_from_string(self.f_date.get())

        try:
            expense_id = self.items['accordance'][self.f_choose.get()]
            amount = float(self.f_amount.get())
            self.l_choose['style'] = "SmpLbl.TLabel"
            self.l_amount['style'] = "SmpLbl.TLabel"
        except KeyError:
            if self.f_choose.get() != "":
                pass
            else:
                flag = False
                self.l_choose['style'] = "ErrLbl.TLabel"
                self.bell()
        except ValueError:
            flag = False
            self.l_amount['style'] = "ErrLbl.TLabel"
            self.bell()

        if flag:
            insert_payment = (amount, payment_date, expense_id)
            if eh.insert_payments(insert_payment):
                self.master.refresh()


class StatFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        l_most_commot_text = ttk.Label(self, text="The most common item")
        l_most_commot_value = ttk.Label(self, text=eh.get_most_common_item(), style="BldLbl.TLabel")
        l_exp_item_text = ttk.Label(self, text="The most expensive item")
        l_exp_item_value = ttk.Label(self, text=eh.get_most_exp_item(), style="BldLbl.TLabel")
        l_exp_day_text = ttk.Label(self, text="The most expensive day")
        l_exp_day_value = ttk.Label(self, text=eh.get_most_exp_day(), style="BldLbl.TLabel")
        l_exp_month_text = ttk.Label(self, text="The most expensive month")
        l_exp_month_value = ttk.Label(self, text=eh.get_most_exp_month(), style="BldLbl.TLabel")

        l_most_commot_text.grid(row="0", column="0", sticky="w")
        l_most_commot_value.grid(row="0", column="1", sticky="e")
        l_exp_item_text.grid(row="1", column="0", sticky="w")
        l_exp_item_value.grid(row="1", column="1", sticky="e")
        l_exp_day_text.grid(row="2", column="0", sticky="w")
        l_exp_day_value.grid(row="2", column="1", sticky="e")
        l_exp_month_text.grid(row="3", column="0", sticky="w")
        l_exp_month_value.grid(row="3", column="1", sticky="e")


class TableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        table = ttk.Treeview(self, show="headings")
        heads = ("id", "name", "amount", "date")
        table['columns'] = heads

        for header in heads:
            table.heading(header, text=header, anchor="center")
            table.column(header, anchor="center")

        for row in eh.get_table_data():
            table.insert('', tk.END, values=row)

        scroll_pane = ttk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scroll_pane.set)
        scroll_pane.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


if __name__ == '__main__':
    app = App()
    app.mainloop()
