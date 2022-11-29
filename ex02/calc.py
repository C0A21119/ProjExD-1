import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt,f"{txt}のボタンが押されました")

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")
j, k = 0, 0
for i in range(9,-1,-1):
    button = tk.Button(root,text=f"{i}",font=("",30),width=4,height=2)
    button.bind("<1>",button_click)
    button.grid(row=j, column=k)
    k += 1
    if k % 3 == 0:
        j += 1
        k = 0


root.mainloop()