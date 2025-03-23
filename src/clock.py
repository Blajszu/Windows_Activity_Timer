import tkinter as tk
import time

class Clock(tk.Label):
    def __init__(self, master, x, y, font=("Roboto Flex", 12, "bold"), text_color="#FFFFFF", bg_color=None):
        super().__init__(
            master,
            font=font,
            fg=text_color,
            bg=bg_color if bg_color else master.background_color,
            bd=0
        )
        self.place(x=x, y=y)
        self.update_time()
    
    def update_time(self):
        current_time = time.strftime("%H:%M")
        self.config(text=current_time)

        self.after(2000, self.update_time)