from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    flag_count = 0
    cell_count_label_object = None
    flag_count_label_object = None
    game_started = False

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_btn_object(self, location):
        dynamic_width = max(10, int(30 / settings.COLS))
        dynamic_height = max(4, int(20 / settings.ROWS))
        btn = Button(
            location,
            width=dynamic_width,
            height=dynamic_height,
            bg="#b9d6f2",
            fg="#000000",
            activebackground="#87bfff",
            relief="raised",
            bd=2
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="#1e3d59",
            fg="#ffffff",
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 20)
        )
        Cell.cell_count_label_object = lbl

    @staticmethod
    def create_flag_count_label(location):
        lbl = Label(
            location,
            bg="#1e3d59",
            fg="#ffcb05",
            text=f"Flags: {Cell.flag_count}/{settings.MINES_COUNT}",
            font=("", 20)
        )
        Cell.flag_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.flood_fill()
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        return [cell for cell in cells if cell is not None]

    @property
    def surrounded_cells_mines_length(self):
        return sum(1 for cell in self.surrounded_cells if cell.is_mine)

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(
                text=self.surrounded_cells_mines_length,
                bg="#f5f0e1",
                fg="black",
                relief="sunken"
            )
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")
        self.is_opened = True

    def flood_fill(self):
        if self.is_opened or self.is_mine:
            return
        self.show_cell()
        if self.surrounded_cells_mines_length == 0:
            for neighbor in self.surrounded_cells:
                if not neighbor.is_opened and not neighbor.is_mine:
                    neighbor.flood_fill()

    def show_mine(self):
        self.cell_btn_object.configure(bg='#d7263d')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            if Cell.flag_count >= settings.MINES_COUNT:
                return
            self.cell_btn_object.configure(bg='#ffcb05')
            self.is_mine_candidate = True
            Cell.flag_count += 1
        else:
            self.cell_btn_object.configure(bg='#b9d6f2')
            self.is_mine_candidate = False
            Cell.flag_count -= 1

        if Cell.flag_count_label_object:
            Cell.flag_count_label_object.configure(
                text=f"Flags: {Cell.flag_count}/{settings.MINES_COUNT}"
            )

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
