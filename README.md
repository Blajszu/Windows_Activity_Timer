# Windows Activity Timer ⏳  

**Windows Activity Timer** is a lightweight Python app that tracks time spent in different programs and includes a simple timer. It monitors user activity in the background and displays statistics for the most frequently used applications. The app has a modern interface and runs quietly in the background.

## 🖥 Screenshot  
<div align="center">
  
  ![Widget_Layout](https://github.com/user-attachments/assets/a2247d3c-c4a2-4082-8bef-a4a17199f0fa)

</div>

## 🚀 Features  
- ⏱ **Timer** – start, pause, and reset functionality.  
- 📊 **Activity Tracking** – logs time spent in active applications.  
- 🎨 **Modern UI** – clean and intuitive layout.  
- 🛠 **Automatic Data Collection** – runs silently in the background.  
- ⚙️ **Custom Configuration** – click the settings button to open `app_config.json` and define app display names and custom icons.  
- 🔁 **Autostart** – the app adds itself to Windows startup automatically after installation, so it runs in the background every time you start your computer.

### 🧩 Configuration Example (`app_config.json`):

Each entry defines how an application should be displayed in the widget.

```json
"msedge.exe": {
    "name": "Microsoft Edge",
    "custom_icon_path": "icons/msedge.png"
}
```

- `name` – the display name for the app  
- `custom_icon_path` – path to a custom icon shown in the widget  

---

## 🏗 Technologies Used  
- **Python 3**  
- **Tkinter** – built-in Python GUI toolkit  
- **Pillow** – for rendering and drawing images (icons, rounded backgrounds, etc.)  
- **psutil** – for process monitoring and tracking activity  
- **pywin32** – for accessing Windows APIs like window titles and processes 

## 📦 Installation  
```bash
git clone https://github.com/user/windows-activity-timer.git
cd windows-activity-timer

pip install -r requirements.txt
python main.py
```

### ⚙️ Autostart on Windows (Automatic):

After installation, the app will automatically add a shortcut to the Windows Startup folder so it launches on boot.

If needed, you can also set it up manually:

1. Press `Win + R`, type `shell:startup`, and press Enter.  
2. Place a shortcut here pointing to your `main.py` or a launcher script.  
3. To use a batch file, create something like this:

```bat
@echo off
cd /d C:\Path\To\windows-activity-timer
python main.py
```

Save it as `start_timer.bat` and place a shortcut to it in the Startup folder.

---

## 📜 License  
This project is licensed under the MIT License.
