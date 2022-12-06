import tkinter as tk
import tkinter.messagebox as tkm
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
    canvas.pack()
    image = tk.PhotoImage(file="fig/0.png")
    canvas.create_image(24,36.5,image=image)

    root.mainloop()