from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=200)
frm.grid()

ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# mainloop() 方法将所有控件显示出来，并响应用户输入直到程序终结
root.mainloop()
