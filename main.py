import tkinter as tk

window = tk.Tk()
window.title('My App')

frame_add_form = tk.Frame(window, width=150, height=150, bg='green')
frame_statistic = tk.Frame(window, width=150, height=150, bg='yellow')
frame_list = tk.Frame(window, width=300, height=150, bg='blue')

frame_add_form.grid(row=0, column=0)
frame_statistic.grid(row=0, column=1)
frame_list.grid(row=1, column=0, columnspan=2)

window.mainloop()