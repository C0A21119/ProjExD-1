import tkinter as tk
import tkinter.messagebox as tkm
import random
import maze_maker as mm
import time

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my
    key_pressed = ["Up","Down","Right","Left"]
    move=[[0,-1],[0,1],[1,0],[-1,0]]
    for i,key_info in enumerate(key_pressed):
        if key == key_info:
            if maze_list[mx+move[i][0]][my+move[i][1]]==0:
                mx += move[i][0]
                my += move[i][1]
    cx, cy = mx*100+50, my*100+50
    canvas.coords("kokaton", cx, cy)
    root.after(100, main_proc)

def time_time():
    global now, tmr
    tmr +=1
    now = tmr
    canvas.create_text(250, 0, text=now,anchor="ne", font=("",50))
    root.after(1000, time_time())

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.place(x=0, y=0)
    canvas.pack()

    maze_list = mm.make_maze(15, 9)
    mm.show_maze(canvas, maze_list)

    tori = tk.PhotoImage(file=random.choice([f"fig/{i}.png" for i in range(10)]))
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    canvas.create_image(cx,cy,image=tori, tag="kokaton")

    now = "-"
    tmr = 0
    canvas.create_text(250, 0, text=now,anchor="ne", font=("",50))

    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyPress>", time_time, "+")
    root.bind("<KeyRelease>", key_up)
    main_proc()
    root.mainloop()