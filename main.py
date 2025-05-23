import tkinter as tk
from tkinter import *
from cell import Cell
import settings
import utils
import time

root = Tk()

# Ukuran layar laptop
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.title("Minesweeper Game")
root.resizable(True, True)  # Bisa di-minimize

root.configure(bg="#1e3d59")
start_time = None
timer_label = None

def update_timer():
    if start_time:
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text=f"⏱️ {elapsed_time}s")
    root.after(1000, update_timer)

top_frame = Frame(root, bg="#3a6073", width=screen_width, height=utils.height_prct(15))
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg="#3a6073",
    fg="white",
    pady=20,
    text='💣 Minesweeper',
    font=('Helvetica', 36, 'bold')
)
game_title.place(relx=0.5, rely=0.1, anchor='n')

timer_label = Label(
    top_frame,
    bg="#3a6073",
    fg="white",
    text="⏱️ 0s",
    font=('Helvetica', 18)
)
timer_label.place(relx=0.9, rely=0.5, anchor='center')

left_frame = Frame(root, bg="#1e3d59", width=utils.width_prct(25), height=utils.height_prct(85))
left_frame.place(x=0, y=utils.height_prct(15))

center_frame = Frame(root, bg="#1e3d59", width=utils.width_prct(75), height=utils.height_prct(85))
center_frame.place(x=utils.width_prct(25), y=utils.height_prct(15))

for x in range(settings.COLS):
    for y in range(settings.ROWS):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=0, y=0)

Cell.create_flag_count_label(left_frame)
Cell.flag_count_label_object.place(x=0, y=50)

Cell.randomize_mines()

def start_game_timer(event):
    global start_time
    if not Cell.game_started:
        Cell.game_started = True
        start_time = time.time()
        update_timer()

for cell in Cell.all:
    cell.cell_btn_object.bind("<Button-1>", lambda event, cell=cell: [start_game_timer(event), cell.left_click_actions(event)])

root.mainloop()
