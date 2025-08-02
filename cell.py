import tkinter as tk


class Cell(tk.Frame):
    def __init__(self, master, bg, fg):
        super().__init__(master, bg=bg)
        self.bg = bg
        self.fg = fg
        self.size = 75
        self.is_number = True
        self.number_frame = tk.Frame(self)
        self.entry = tk.Entry(self.number_frame)
        self._set_frame()
        self._set_entry()

    def _set_frame(self):
        self.number_frame.config(bg=self.bg, width=self.size, height=self.size,
                                 highlightbackground=self.bg,
                                 highlightcolor=self.fg,
                                 highlightthickness=1)
        self.number_frame.grid(row=0, column=0, padx=2, pady=2)

    def _set_entry(self):
        self.entry.config(bg=self.bg, font=("Arial", 25, "bold"),
                          fg=self.fg, justify="center", bd=0)
        self.entry.place(relx=0.5, rely=0.5, anchor="center")

    def switch_font(self):
        if self.is_number:
            self.entry.config(font=("Arial", 25, "bold"))
        else:
            self.entry.config(font=("Arial", 11, "normal"))