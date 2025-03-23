import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class TimerButton(tk.Label):
    def __init__(
        self,
        master,
        position=(0, 0),
        size=(46, 19),
        corner_radius=6,
        background_color="#454545",
        parent_bg="#323232",
        text=None,
        font=("Roboto Flex", 12, "bold"),
        text_color="#FFFFFF",
        command=None
    ):
        super().__init__(
            master,
            font=font,
            fg=text_color,
            bg=background_color,
            bd=0,
            text=text
        )

        self.text = text
        self.font = font
        self.text_color = text_color
        self.position = position
        self.size = size
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.parent_bg = parent_bg
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

        if self.text:

            self.text_label = tk.Label(
                self.master,
                text=self.text,
                font=self.font,
                fg=self.text_color,
                bg=self.background_color,
                bd=0,
                cursor="hand2"
            )
            
            text_x = self.position[0] + (self.size[0] // 2)
            text_y = self.position[1] + (self.size[1] // 2)
            
            self.text_label.place(x=text_x, y=text_y, anchor="center")
            
            if self.command:
                self.text_label.bind("<Button-1>", lambda event: self.command())
        
        