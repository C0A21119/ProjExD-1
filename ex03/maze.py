import tkinter as tk
import tkinter.messagebox as tkm
import maze_maker

def key_doen(event):
    key = event.keysym
    root.after(1000, )


def key_up(event):
    key = ""

key = ""

root = tk.Tk()
root.title("迷えるこうかとん")
root.geometry("1500x900")

canvas = tk.Canvas(1500,900,bg="black")
canvas.pack()
image = tk.PhotoImage(file="0.png")
canvas.create_image(24,36.5,image=image)

root.mainloop()