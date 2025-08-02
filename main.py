import tkinter as tk
from tkinter import messagebox

from field import Field


def main():
    window = tk.Tk()
    colors = ["#3b3b3b", "#9da1aa", "#70737a"]
    set_window(window, colors[0])
    field = get_field(window, colors)
    set_menu(window, field)
    window.mainloop()


def set_window(window, window_bg):
    window.title("Sudoku Game")
    window.wm_iconphoto(False, tk.PhotoImage(file='sudoku_icon.png'))
    window.config(bg=window_bg)
    window.state("zoomed")


def set_menu(window, field):
    menu = tk.Menu(window)
    window.config(menu=menu)
    menu.add_command(label="New Game", command=lambda: new_game(field))
    menu.add_command(label="Exit", command=lambda: end_game(window))
    menu.add_command(label="Info", command=show_info)

def get_field(window, colors):
    field = Field(window, size=750, bg="#5d6970", colors=colors)
    field.pack_propagate(False)
    field.place(relx=0.5, rely=0.5, anchor="center")
    return field


def new_game(field):
    response = messagebox.askyesno(title="New Game", message="Do you really want to start a new game?")
    if response:
        field.new_game()


def end_game(window):
    response = messagebox.askyesno(title="Exit", message="Do you really want to quit?")
    if response:
        window.destroy()

def show_info():
    info_text = (
        "Controls:\n"
        "- Arrow keys: Move between cells\n"
        "- Enter a number: Input a number into the selected cell\n"
        "- Ctrl + number: Add or remove a note in the cell\n"
        "- Space: Show errors\n"
        "- 'New Game' in the menu starts a new game\n"
        "- 'Exit' in the menu quits the game"
    )
    messagebox.showinfo("Game Controls", info_text)

if __name__ == "__main__":
    main()