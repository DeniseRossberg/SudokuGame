import tkinter as tk
from game import Game


class Field(tk.Frame):
    def __init__(self, master, size, bg, colors):
        super().__init__(master, width=size, height=size, bg=bg)
        self.colors = colors
        self.start_frame = tk.Frame(self, bg=bg, width=size, height=size)
        self.game_frame = tk.Frame(self, bg=bg, width=size, height=size)
        self.game = None
        self.buttons = []
        self.button_frame = tk.Frame(self.start_frame, bg=bg, width=size, height=size)
        self.button_frame.pack(expand=True)
        self._set_start_frame()
        self._set_game_frame()

    def _set_buttons(self):
        self.buttons = [tk.Button(self.button_frame, text="Easy"),
                        tk.Button(self.button_frame, text="Medium"),
                        tk.Button(self.button_frame, text="Hard")]

        for btn in self.buttons:
            btn.config(font=("Arial", 15, "bold"),
                       background=self.colors[0],
                       activebackground=self.colors[0],
                       fg=self.colors[1],
                       width=15,
                       command=lambda difficulty=btn["text"]: self.play(difficulty.lower()))
            btn.pack(anchor="center", pady=5)

    def _set_start_frame(self):
        self._set_buttons()
        self.start_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.start_frame.pack_propagate(False)
        self.start_frame.tkraise()

    def _set_game_frame(self):
        self.game_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.game_frame.pack_propagate(False)

    def play(self, difficulty):
        self.game = Game(self.game_frame, difficulty, self.colors[0],
                         self.colors[1], self.colors[2], self.new_game)
        self.game.play()
        self.game_frame.tkraise()

    def new_game(self):
        self.start_frame.tkraise()
