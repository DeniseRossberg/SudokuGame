import tkinter
from tkinter import messagebox

from sudoku_generator import Sudoku
from cell import Cell


class Game:
    def __init__(self, master, difficulty, bg, fg, inactive_fg, new_game):
        self.puzzle, self.solution = Sudoku.get_sudoku(difficulty)
        self.master = master
        self.bg = bg
        self.fg = fg
        self.inactive_fg = inactive_fg
        self.new_game = new_game
        self.cells = []
        self.error_cells = []
        self.active_x = 0
        self.active_y = 0

    def _set_master(self):
        self.master.bind("<KeyPress>", self._on_key_press)
        self.master.bind_all("<KeyRelease>", self._on_key_release)
        self.master.focus_set()

    def _set_cells(self):
        for i in range(9):
            row = []
            for j in range(9):
                cell = Cell(self.master, bg=self.bg, fg=self.fg)
                padx = 1
                pady = 1
                if j in (2, 5):
                    padx = (padx, 7)
                if i in (2, 5):
                    pady = (pady, 7)

                cell.grid(row=i, column=j, padx=padx, pady=pady)
                row.append(cell)
            self.cells.append(row)

    def _fill_cells(self):
        for i in range(9):
            for j in range(9):
                num = self.puzzle[i][j]
                cell = self.cells[i][j]
                cell.entry.bind("<Key>", self._on_key_press)
                cell.entry.bind("<FocusIn>", lambda e, row=i, col=j:
                self._on_entry_focus(row, col))
                if num != 0:
                    cell.entry.insert(0, str(num))
                    cell.entry.config(fg=self.inactive_fg)
                cell.entry.config(state="readonly", readonlybackground=self.bg)

    def _move(self, event):
        if event.keysym == "Up":
            self.active_x = (self.active_x - 1) % 9
        elif event.keysym == "Down":
            self.active_x = (self.active_x + 1) % 9
        elif event.keysym == "Left":
            self.active_y = (self.active_y - 1) % 9
        elif event.keysym == "Right":
            self.active_y = (self.active_y + 1) % 9
        self.cells[self.active_x][self.active_y].entry.focus_set()

    def _write_number(self, num):
        cell = self.cells[self.active_x][self.active_y]
        cell.is_number = True
        cell.switch_font()
        self.puzzle[self.active_x][self.active_y] = int(num)
        cell.entry.config(state="normal")
        cell.entry.delete(0, tkinter.END)
        cell.entry.insert(0, num)
        cell.entry.config(state="readonly",
                          readonlybackground=self.bg)
        self._check_solution()

    def _delete_number(self):
        cell = self.cells[self.active_x][self.active_y]
        self.puzzle[self.active_x][self.active_y] = 0
        cell.entry.config(state="normal")
        cell.entry.delete(len(cell.entry.get()) - 1)
        cell.entry.config(state="readonly",
                          readonlybackground=self.bg)

    def _write_note(self, num):
        cell = self.cells[self.active_x][self.active_y]
        if cell.is_number and cell.entry.get() != "":
            return

        cell.is_number = False
        cell.switch_font()
        cell.entry.config(state="normal")
        current_notes = cell.entry.get()
        num_str = str(num)

        if num_str in current_notes:
            new_notes = current_notes.replace(num_str, "")
        else:
            new_notes = current_notes + num_str

        new_notes = ''.join(sorted(new_notes))
        cell.entry.delete(0, "end")
        cell.entry.insert(0, new_notes)
        cell.entry.config(state="readonly")

    def _on_key_press(self, event):
        ctrl = (event.state & 0x4) != 0
        num = event.keysym.replace("KP_", "")

        if event.keysym in ("Up", "Down", "Left", "Right"):
            self._move(event)
        elif num in map(str, range(1, 10)):
            if ctrl:
                self._write_note(num)
            else:
                self._write_number(num)
        elif event.keysym == "BackSpace":
            self._delete_number()
        elif event.keysym == "space":
            self._show_errors()
        else:
            return

    def _on_key_release(self, event):
        if event.keysym == "space":
            self._reset_highlight()

    def _show_errors(self):
        for i in range(9):
            for j in range(9):
                num = self.puzzle[i][j]
                cell = self.cells[i][j]
                if num != 0 and num != self.solution[i][j]:
                    self.error_cells.append(cell)
                    cell.entry.config(fg="red")

    def _reset_highlight(self):
        for cell in self.error_cells:
            cell.entry.config(fg=self.fg)
        self.error_cells = []

    def _on_entry_focus(self, row, col):
        self.active_x = row
        self.active_y = col

    def _check_solution(self):
        if (self.puzzle == self.solution).all():
            messagebox.showinfo("Congratulations!", "You solved the sudoku puzzle!")
            self.new_game()

    def play(self):
        self._set_master()
        self._set_cells()
        self._fill_cells()
        self.cells[self.active_x][self.active_y].entry.focus_set()
