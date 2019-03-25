# coding: utf-8
import tkinter
root = tkinter.Tk()
root.title('Hello, World!')
root.geometry('250x50+20+20')
lb1 = tkinter.Label(root,text='Hello, World!',font='144')
lb1.pack(fill='both',expand=True)
root.mainloop()