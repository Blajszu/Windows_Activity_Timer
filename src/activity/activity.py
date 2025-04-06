import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from activity.app_tracker import AppTracker

class TopAppsWidget(tk.Label):
    def __init__(
            self, 
            master, 
            position=(0, 0), 
            corner_radius=10, 
            size=(300, 200), 
            background_color="#454545", 
            text_color="white",
            parent_bg="#323232",
            title="Top 4 Apps",
            update_interval=1
        ):
        super().__init__(master)
        self.width = size[0]
        self.height = size[1]
        self.corner_radius = corner_radius
        self.background_color = background_color
        self.text_color = text_color
        self.parent_bg = parent_bg
        self.title = title
        self.position = position
        self.labels = []
        self.icons = []
        self.update_interval = update_interval
        
        self.app_tracker = AppTracker(config_file="src/app_config.json")
        self.top_apps = []
        
        self.place(x=position[0], y=position[1])
        self.create_widget_image()
        self.create_title()
        self.create_apps_list()
        
        self.start_tracking()

    def start_tracking(self):
        self.track_apps()
        self.update_widget()

    def track_apps(self):
        self.app_tracker.track()
        self.after(1000, self.track_apps)

    def update_widget(self):
        self.top_apps = self.app_tracker.get_top_apps()
        self.update_apps_data(self.top_apps)
        self.create_title()
        self.after(self.update_interval * 1000, self.update_widget)

    def create_widget_image(self):
        widget_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(widget_image)
        
        draw.rounded_rectangle(
            (0, 0, self.width, self.height),
            radius=self.corner_radius,
            fill=self.background_color
        )
        
        self.widget_image = ImageTk.PhotoImage(widget_image)
        self.configure(image=self.widget_image, bg=self.parent_bg)

    def create_title(self):
        self.title_label = tk.Label(
            self,
            text=self.title,
            fg=self.text_color,
            bg=self.background_color,
            font=("Roboto Flex", 8, "bold")
        )
        self.title_label.place(x=18, y=6)

    def create_apps_list(self):
        for i, app in enumerate(self.top_apps):
            img = Image.new("RGBA", (self.width-8, 23), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle(
                (0, 0, self.width-10, 22),
                radius=5,
                fill="#555555"
            )
            img_tk = ImageTk.PhotoImage(img)
            self.labels.append(img_tk)

            canvas = tk.Canvas(
                self,
                width=self.width-8,
                height=23,
                bd=0,
                highlightthickness=0,
                bg=self.background_color
            )
            canvas.create_image(0, 0, image=img_tk, anchor="nw")
            
            if "icon" in app and app["icon"]:
                canvas.create_image(
                    4, 11,
                    image=app["icon"],
                    anchor="w"
                )
                self.icons.append(app["icon"])
                text_x = 25
            else:
                text_x = 4
            
            canvas.create_text(
                text_x, 2,
                text=app["name"], 
                fill=self.text_color, 
                font=("Roboto Flex", 6), 
                anchor="nw"
            )
            
            canvas.create_text(
                self.width-14, 22,
                text=app["time"], 
                fill=self.text_color, 
                font=("Roboto Flex", 6), 
                anchor="se"
            )
            
            canvas.place(x=4, y=33 + i*25)

    def update_apps_data(self, new_apps_data):
        self.top_apps = new_apps_data
        for child in self.winfo_children():
            if child not in [self.title_label]:
                child.destroy()
        self.labels.clear()
        self.icons.clear()
        self.create_apps_list()