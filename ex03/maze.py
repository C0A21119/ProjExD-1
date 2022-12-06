import tkinter as tk
import tkinter.messagebox as tkm
import random
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym
    if now == "-":
        root.after(100, time_time)

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my, key
    key_pressed = ["Up","Down","Right","Left"]
    move=[[0,-1],[0,1],[1,0],[-1,0]]
    for i,key_info in enumerate(key_pressed):
        if key == key_info:
            if maze_list[mx+move[i][0]][my+move[i][1]]==0 or maze_list[mx+move[i][0]][my+move[i][1]]==2:
                mx += move[i][0]
                my += move[i][1]
                cx, cy = mx*100+50, my*100+50
                canvas.coords("kokaton", cx, cy)
            else:
                canvas.coords("kokaton", cx, cy)
    if maze_list[mx][my] == 2:
        key = ""
        mx, my = 1, 1
        cx, cy = mx*100+50, my*100+50
        emx, emy = 14, 7
        ex, ey = emx*100+50, emy*100+50
        canvas.delete("text")
        canvas.coords("kokaton", cx, cy)
        canvas.coords("enemey",ex, ey)
        tkm.showinfo("ゴール達成", f"GOAL time{now}")
        exit()
    enemy_move()
    root.after(100, main_proc)


def enemy_move(): #enemyを動かす関数
    global maze_list, canvas, mx, my, emx, emy, cx, cy
    e_moves=[[0,-1],[0,1],[1,0],[-1,0]]
    e_move = random.choice(["Up", "Down", "Left", "Right"])
    key_pressed = ["Up","Down","Right","Left"]
    try:
        for i,key_info in enumerate(key_pressed):
            if e_move == key_info:
                if maze_list[emx+e_moves[i][0]][emy+e_moves[i][1]]==0:
                    emx += e_moves[i][0]
                    emy += e_moves[i][1]
    except:
        pass
    ex, ey = emx*100+50, emy*100+50
    canvas.coords("enemey",ex, ey)
    if ex == cx and ey == cy:
        key = ""
        mx, my = 1, 1
        cx, cy = mx*100+50, my*100+50
        emx, emy = 14, 7
        ex, ey = emx*100+50, emy*100+50
        canvas.coords("kokaton", cx, cy)
        canvas.coords("enemey",ex, ey)
        canvas.delete("text")
        tkm.showinfo("ゴール失敗", f"GOALOVER time{now}")


def time_time():
    global now, tmr
    canvas.delete("text")
    tmr += 1
    now = tmr
    canvas.create_text(250, 0, text=now,anchor="ne", font=("",50), tag="text")
    jid = root.after(1000, time_time)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    canvas = tk.Canvas(root,width=1500,height=900,bg="black")
    canvas.place(x=0, y=0)
    canvas.pack()

    maze_list = mm.make_maze(15, 9)
    mm.show_maze(canvas, maze_list)

    tori = tk.PhotoImage(file=random.choice([f"fig/{i}.png" for i in range(10)]))
    enemey = tk.PhotoImage(file=random.choice([f"fig/{i}.png" for i in range(10)]))
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    emx, emy = 14, 7
    ex, ey = emx*100+50, emy*100+50
    canvas.create_image(cx,cy,image=tori, tag="kokaton")
    canvas.create_image(ex,ey,image=enemey, tag="enemey")

    now = "-"
    tmr = 0
    canvas.create_text(250, 0, text=now,anchor="ne", font=("",50),tag= "text")

    key = ""
    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()
    root.mainloop()