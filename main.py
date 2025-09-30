import tkinter as tk
import expenses_helper as eh

window = tk.Tk()
window.title("My App")

frame_add_form = tk.Frame(window, bg="green")
frame_statistic = tk.Frame(window, bg="yellow")
frame_list = tk.Frame(window, bg="blue")

frame_add_form.grid(row=0, column=0, sticky="ns")
frame_statistic.grid(row=0, column=1)
frame_list.grid(row=1, column=0, columnspan=2, sticky="we")

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

l_temp_frame_add_form = tk.Label(frame_add_form, text="frame_add_form")
l_temp_frame_list = tk.Label(frame_list, text="frame_list")
l_temp_frame_add_form.pack(expand=True, padx=20, pady=20)
l_temp_frame_list.pack(expand=True, padx=20, pady=20)

window.mainloop()
