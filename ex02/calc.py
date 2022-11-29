import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt,f"{txt}のボタンが押されました")

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")

button9 = tk.Button(root,text="9",font=30,width=4,height=2)
button9.bind("<1>",button_click)
button8 = tk.Button(root,text="8",font=30,width=4,height=2)
button8.bind("<1>",button_click)
button7 = tk.Button(root,text="7",font=30,width=4,height=2)
button7.bind("<1>",button_click)
button6 = tk.Button(root,text="6",font=30,width=4,height=2)
button6.bind("<1>",button_click)
button5 = tk.Button(root,text="5",font=30,width=4,height=2)
button5.bind("<1>",button_click)
button4 = tk.Button(root,text="4",font=30,width=4,height=2)
button4.bind("<1>",button_click)
button3 = tk.Button(root,text="3",font=30,width=4,height=2)
button3.bind("<1>",button_click)
button2 = tk.Button(root,text="2",font=30,width=4,height=2)
button2.bind("<1>",button_click)
button1 = tk.Button(root,text="1",font=30,width=4,height=2)
button1.bind("<1>",button_click)

button9.grid(row=0, column=0)
button8.grid(row=0, column=1)
button7.grid(row=0, column=2)
button6.grid(row=1, column=0)
button5.grid(row=1, column=1)
button4.grid(row=1, column=2)
button3.grid(row=2, column=0)
button2.grid(row=2, column=1)
button1.grid(row=2, column=2)


root.mainloop()