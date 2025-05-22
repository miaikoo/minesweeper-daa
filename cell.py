from tkinter import Button, Label
import random
import settings
import ctypes
import sys
import time

game_started = False

class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    flag_count = 0
    cell_count_label_object = None
    flag_count_label_object = None
    game_started = False
    timer_label = None

    def __init__(self,x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to the Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        dynamic_width = max(10, int(30 / settings.COLS)) 
        dynamic_height = max(4, int(20 / settings.ROWS))
        btn = Button(
            location,
            width=dynamic_width,
            height=dynamic_height,
        )
        btn.bind('<Button-1>', self.left_click_actions ) # Left Click
        btn.bind('<Button-3>', self.right_click_actions ) # Right Click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 20)
        )
        Cell.cell_count_label_object = lbl
    
    @staticmethod
    def create_flag_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='orange',
            text=f"Flags: {Cell.flag_count}/{settings.MINES_COUNT}",
            font=("", 20)
        )
        Cell.flag_count_label_object = lbl

    @staticmethod
    def create_timer_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='cyan',
            text="Time: 0s",
            font=("", 20)
        )
        Cell.timer_label = lbl
    
    @staticmethod
    def update_timer():
        if Cell.game_started and Cell.timer_label:
            elapsed = int(time.time() - Cell.start_time)
            Cell.timer_label.config(text=f"Time: {elapsed}s")
            Cell.timer_label.after(1000, Cell.update_timer)

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.flood_fill()
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game!', 'Game Over', 0)

        # Cancel Left and Right click events if cell is already opened:
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x,y):
        # Return a cell object based on the value of x,y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y -1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this was a mine candidate, then for safety, we should
            # configure the background color to SystemButtonFace
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )

        # Mark the cell as opened (Use is as the last line of this method)
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
        self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()


    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            if not self.is_mine_candidate and Cell.flag_count >= settings.MINES_COUNT:
                return
            
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
            Cell.flag_count += 1
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False
            Cell.flag_count -= 1

        if Cell.flag_count_label_object:
            Cell.flag_count_label_object.configure(
            text=f"Flags: {Cell.flag_count}/{settings.MINES_COUNT}"
        )

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
