import tkinter as tk
import tkinter.messagebox as tkm
import math


def button_C():
    entry.delete(0,tk.END)

def button_sin():
    res = math.sin(math.radians(eval(entry.get())))
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_cos():
    res = math.cos(math.radians(eval(entry.get())))
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_tan():
    res = math.tan(math.radians(eval(entry.get())))
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_π():
    res = "3.14"
    entry.insert(tk.END,res)

def button_x2():
    res = eval("("+entry.get()+")**2")
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_xn():
    res = math.factorial(eval(entry.get()))
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_1():
    res = eval("1/"+entry.get())
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_sq():
    res = math.sqrt(eval(entry.get()))
    entry.delete(0,tk.END)
    entry.insert(tk.END,res)

def button_click(event):
    try:
        btn = event.widget
        txt = btn["text"]
        if txt == "=":
            res = eval(entry.get())
            entry.delete(0,tk.END)
            entry.insert(tk.END,res)
        elif txt == "x":
            entry.insert(tk.END,"*")
        elif txt == "÷":
            entry.insert(tk.END,"/")
        elif txt == "C":
            button_C()
        elif txt == "sin":
            button_sin()
        elif txt == "cos":
            button_cos()
        elif txt == "tan":
            button_tan()
        elif txt == "π":
            button_π()
        elif txt == "x^2":
            button_x2()
        elif txt == "x!":
            button_xn()
        elif txt == "1/x":
            button_1()
        elif txt == "√":
            button_sq()
        else:
            entry.insert(tk.END,txt)
    except SyntaxError:
        entry.delete(0,tk.END)
        entry.insert(tk.END,"数式が間違っています")


root = tk.Tk()
root.title("電卓")
root.geometry("575x600")


j, k = 1, 0
for num in ["sin","cos","tan","√","π",
            7,8,9,"÷","x^2",
            4,5,6,"x","x!",
            1,2,3,"-","1/x",
            0,".","=","+","C"]:
    button = tk.Button(root,text=f"{num}",font=("",30),width=5,height=2,bg="lightgrey")
    button.bind("<1>",button_click)#右クリックがされたとき
    button.grid(row=j, column=k)
    k +=1
    if k % 5 == 0:
        j += 1
        k = 0

entry = tk.Entry(root,justify="right",width=20,font=("",40))
entry.grid(row=0,column=0, columnspan=5)


root.mainloop()