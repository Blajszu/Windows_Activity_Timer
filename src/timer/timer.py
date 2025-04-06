import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from timer.timer_button import TimerButton
import time

class Timer(tk.Label):
    def __init__(
            self, 
            master, 
            position=(0, 0), 
            corner_radius=15, 
            size=(170, 170), 
            background_color="#454545", 
            circle_color="#46DD76",
            parent_bg="#323232"
        ):
        super().__init__(master)
        self.width = size[0]
        self.height = size[1]
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.circle_color = circle_color
        self.parent_bg = parent_bg
        self.position = position
        
        self.place(x=position[0], y=position[1])

        self.time_elapsed = 0
        self.running = False
        self.start_time = None
        self.rotation_angle = 0
        self.circle_image_path = "src/img/timer_circle.png"
        self.current_button_creator = None
        self.current_button = None

        self.create_timer_image()
        self.set_start_button()
        self.display_time(position=(140, 70), font_size=25)

    def create_timer_image(self):

        timer_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(timer_image)
        
        draw.rounded_rectangle(
            (0, 0, self.width, self.height),
            radius=self.corner_radius,
            fill=self.background_color
        )
        
        circle_overlay = Image.open(self.circle_image_path)
        circle_overlay = circle_overlay.resize((self.width - 10, self.height - 10), Image.LANCZOS)
        rotated_circle = circle_overlay.rotate(self.rotation_angle, resample=Image.BICUBIC)
        timer_image.paste(rotated_circle, (5, 5), rotated_circle)
        
        self.timer_image = ImageTk.PhotoImage(timer_image)
        self.configure(image=self.timer_image, bg=self.parent_bg)

    def _clear_current_button(self):

        if self.current_button and self.current_button.winfo_exists():
            self.current_button.destroy()
        self.create_timer_image()

    def set_start_button(self):
        self._update_button_state(self._create_start_button)

    def set_stop_button(self):
        self._update_button_state(self._create_stop_button)

    def set_reset_and_end_buttons(self):
        self._update_button_state(self._create_reset_and_end_buttons)

    def _update_button_state(self, creator):

        self.current_button_creator = creator
        self._clear_current_button()
        self.current_button_creator()
        self.create_timer_image()

    def _create_start_button(self):
        self.current_button = TimerButton(
            master=self,
            position=(62, 115),
            size=(46, 19),
            corner_radius=8,
            background_color="#46DD76",
            parent_bg=self.background_color,
            text="START",
            font=("Roboto Flex", 8, "bold"),
            text_color="#FFFFFF",
            command=self.start
        )

    def _create_stop_button(self):
        self.current_button = TimerButton(
            master=self,
            position=(62, 115),
            size=(46, 19),
            corner_radius=8,
            background_color="#DD4B46",
            parent_bg=self.background_color,
            text="STOP",
            font=("Roboto Flex", 8, "bold"),
            text_color="#FFFFFF",
            command=self.stop
        )

    def _create_reset_and_end_buttons(self):

        container = tk.Frame(self, bg=self.background_color)
        container.place(x=38, y=115, width=100, height=19)
        
        self.reset_btn = TimerButton(
            master=container,
            position=(0, 0),
            size=(46, 19),
            corner_radius=8,
            background_color="#DDBF46",
            parent_bg=self.background_color,
            text="RESET",
            font=("Roboto Flex", 8, "bold"),
            text_color="#FFFFFF",
            command=self.resume
        )

        self.end_btn = TimerButton(
            master=container,
            position=(50, 0),
            size=(46, 19),
            corner_radius=8,
            background_color="#DD4B46",
            parent_bg=self.background_color,
            text="END",
            font=("Roboto Flex", 8, "bold"),
            text_color="#FFFFFF",
            command=self.reset
        )
        
        self.current_button = container

    def switch_to_small_circle(self):
        self.circle_image_path = "src/img/timer_small_circle.png"
        self.create_timer_image()

    def switch_to_normal_circle(self):
        self.circle_image_path = "src/img/timer_circle.png"
        self.create_timer_image()

    def update_display(self):
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        milliseconds = (self.time_elapsed * 100) % 100
        
        self.text = f"{minutes:02}:{seconds:02}:{milliseconds:02}"
        self.configure(text=self.text, fg="white", font=("Roboto Flex", 16, "bold"))

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            self.time_elapsed = int(elapsed * 100) // 100
            
            self.rotate_circle()
            self.update_display()
            self.display_time(position=(100, 80), font_size=16)
            self.set_stop_button()
            
            self.after(1000, self.update_timer)

    def display_time(self, position=(0, 0), font_size=12):
        hours = self.time_elapsed // 3600
        minutes = (self.time_elapsed % 3600) // 60
        seconds = self.time_elapsed % 60
        
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        
        if hasattr(self, 'time_label_hms'):
            self.time_label_hms.config(text=time_str)
        else:
            self.time_label_hms = tk.Label(
                self.master,
                text=time_str,
                fg="white",
                bg=self.background_color,
                font=("Roboto Flex", font_size, "bold")
            )
            self.time_label_hms.place(x=position[0], y=position[1])
        
        return self.time_label_hms
    
    def rotate_circle(self):
        self.rotation_angle = (self.time_elapsed * -6) % 360
        self.create_timer_image()

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.time_elapsed
            self.switch_to_small_circle()
            self.set_stop_button()
            self.update_timer()
    
    def stop(self):
        if self.running:
            self.running = False
            self.set_reset_and_end_buttons()
    
    def resume(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.time_elapsed
            self.set_stop_button()
            self.update_timer()
        
    def reset(self):
        self.switch_to_normal_circle()
        self.set_start_button()
        self.running = False
        self.time_elapsed = 0
        self.rotation_angle = 0
        self.create_timer_image()
        self.display_time(position=(100, 80), font_size=16)
