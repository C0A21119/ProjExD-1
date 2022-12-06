import tkinter as tk
import tkinter.messagebox as tkm
import random
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy
    key_pressed = ["Up","Down","Right","Left"]
    #move=[[0,-1],[0,1],[1,0],[-1,0]]
    move=[[0,-20],[0,20],[20,0],[-20,0]]
    for i,key_info in enumerate(key_pressed):
        if key == key_info:
            cx += move[i][0]
            cy += move[i][1]
    canvas.coords("kokaton", cx, cy)
    root.after(100, main_proc)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.place(x=0, y=0)
    canvas.pack()

    maze_list = mm.make_maze(15, 9)
    mm.show_maze(canvas, maze_list)

    tori = tk.PhotoImage(file=random.choice([f"fig/{i}.png" for i in range(10)]))
    cx, cy = 300, 400
    canvas.create_image(cx,cy,image=tori, tag="kokaton")
    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    root.mainloop()