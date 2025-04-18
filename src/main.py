import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from custom_button import CustomButton
from clock import Clock
from timer.timer import Timer
from activity.activity import TopAppsWidget
import os
import platform

class CustomWindow(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)
        
        self.window_width = 300
        self.window_height = 185
        self.corner_radius = 15
        self.background_color = "#323232"
        self.transparent_color = "#000000"
        
        self._offsetx = 0
        self._offsety = 0
        
        self._setup_window()
        self._create_background()
        self._create_buttons()
        self._create_timer()
        self._create_clock()
        self._create_activity()
        self._position_window()
        
    def _setup_window(self):

        self.geometry(f"{self.window_width}x{self.window_height}")
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", self.transparent_color)
        
    def _create_background(self):

        image = Image.new("RGBA", (self.window_width, self.window_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (0, 0, self.window_width, self.window_height), 
            radius=self.corner_radius, 
            fill=self.background_color
        )
        
        self.bg_image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(
            self, 
            width=self.window_width, 
            height=self.window_height, 
            bg=self.transparent_color, 
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.canvas.bind('<Button-1>', self._start_drag)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        
    def _create_buttons(self):

        self.close_button = CustomButton(
            master=self,
            position=(8, 8),
            size=(20, 20),
            corner_radius=6,
            background_color="#454545",
            parent_bg=self.background_color,
            icon_path="src/img/close_icon.png",
            icon_size=(18, 18),
            command=self.quit
        )
        
        self.settings_button = CustomButton(
            master=self,
            position=(33, 8),
            size=(20, 20),
            corner_radius=6,
            background_color="#454545",
            parent_bg=self.background_color,
            icon_path="src/img/settings_icon.png",
            icon_size=(18, 18),
            command=self._open_settings
        )
    
    def _open_settings(self):

            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(BASE_DIR, 'app_config.json')

            if platform.system() == 'Windows':
                os.startfile(config_path)

    def _create_timer(self):
        self.timer = Timer(
            master=self,
            position=(120, 6),
            size=(170, 170),
            corner_radius=15,
            background_color="#454545",
            circle_color="#46DD76",
            parent_bg="#323232"
        )
        
    def _create_clock(self):

        clock_x = 60
        clock_y = 9
        
        self.clock = Clock(
            master=self,
            x=clock_x,
            y=clock_y,
            font=("Roboto Flex", 10, "bold"),
            text_color="#FFFFFF"
        )

    def _create_activity(self):
        self.top_apps_widget = TopAppsWidget(
            master=self,
            position=(6, 40),
            size=(105, 135)
        )
        
    def _position_window(self):

        screen_width = self.winfo_screenwidth()
        x_offset = -10
        y_offset = 10
        
        x = screen_width - self.window_width + x_offset
        y = 0 + y_offset
        
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
            
    def _start_drag(self, event):

        self._offsetx = event.x
        self._offsety = event.y
        
    def _on_drag(self, event):

        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    window = CustomWindow()
    window.mainloop()