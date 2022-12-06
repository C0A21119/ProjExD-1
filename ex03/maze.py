import tkinter as tk
import tkinter.messagebox as tkm
import random
import maze_maker

def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.place(x=0, y=0)
    canvas.pack()
    tori = tk.PhotoImage(file=random.choice([f"fig/{i}.png" for i in range(10)]))
    cx, cy = 300, 400
    canvas.create_image(cx,cy,image=tori, tag="kokaton")
    key = ""

    root.mainloop()