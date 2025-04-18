import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import os

class CustomButton:
    def __init__(
        self,
        master,
        position=(0, 0),
        size=(20, 20),
        corner_radius=6,
        background_color="#454545",
        parent_bg="#323232",
        icon_path=None,
        icon_size=(18, 18),
        command=None
    ):

        self.master = master
        self.position = position
        self.size = size
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.parent_bg = parent_bg
        self.icon_path = icon_path
        self.icon_size = icon_size
        self.command = command
        
        self._create_button()
        
    def _create_button(self):
        button_image = Image.new("RGBA", self.size, (0, 0, 0, 0))
        button_draw = ImageDraw.Draw(button_image)
        button_draw.rounded_rectangle(
            (-1, -1, self.size[0], self.size[1]),
            radius=self.corner_radius,
            fill=self.background_color
        )
        self.button_img = ImageTk.PhotoImage(button_image)
        
        self.button = tk.Label(
            self.master,
            image=self.button_img,
            cursor="hand2",
            bd=0,
            bg=self.parent_bg
        )
        self.button.place(x=self.position[0], y=self.position[1])
        
        if self.command:
            self.button.bind("<Button-1>", lambda event: self.command())
        
        if self.icon_path and os.path.exists(self.icon_path):
            icon = Image.open(self.icon_path).resize(self.icon_size)
            self.icon_img = ImageTk.PhotoImage(icon)
            
            self.icon_label = tk.Label(
                self.button,
                image=self.icon_img,
                bd=0,
                bg=self.background_color
            )
            self.icon_label.place(relx=0.5, rely=0.5, anchor="center")
            
            if self.command:
                self.icon_label.bind("<Button-1>", lambda event: self.command())
        elif self.icon_path:
            print(f"Warning: Icon not found at {self.icon_path}")