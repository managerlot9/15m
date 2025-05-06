import tkinter as tk
from tkinter import messagebox, PhotoImage
import json
from datetime import datetime
import os

class CountdownApp:

    def __init__(self, root):
        """
        Инициализирует главное окно приложения, виджеты и загружает данные.

        Args:
            root (tk.Tk): Корневое окно tkinter.
        """
        self.root = root
        self.root.title("15:00")

        # Загрузка иконки приложения
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "working.png")
            self.app_icon = PhotoImage(file=icon_path)
            root.iconphoto(True, self.app_icon)
        except Exception as e:
            print(f"Application icon not loaded: {e}")

        # Загрузка иконок для кнопок
        try:
            self.start_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "start.png"))
            self.pause_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "pause.png"))
            self.stats_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "stat.png"))
        except Exception as e:
            print(f"Error loading button icons: {e}")
            self.start_img = None
            self.pause_img = None
            self.stats_img = None

        self.label = tk.Label(root, text="15:00", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.today_label = tk.Label(root, text="Today: 0 h 0 min", font=("Helvetica", 8), anchor=tk.E)
        self.today_label.pack(side=tk.TOP, fill=tk.X)

        self.start_button = tk.Button(root, image=self.start_img, command=self.start_countdown, text="", compound=tk.CENTER)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(root, image=self.pause_img, command=self.pause_countdown, text="", compound=tk.CENTER)
        self.pause_button.pack(side=tk.RIGHT, padx=10)

        self.stat_button = tk.Button(root, image=self.stats_img, command=self.show_statistics)
        self.stat_button.pack(side=tk.BOTTOM, pady=10)

        self.running = False
        self.paused = False
        self.remaining = 900  # 15 minutes in seconds
        self.cycle_count = 0
        self.default_bg = root.cget('bg')
        self.data_file = os.path.join(os.path.dirname(__file__), 'countdown_data_15.json')
        self.load_data()
        self.update_today_label()

    def load_data(self):
        """Loads cycle statistics data from a JSON file."""
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        """Saves the current cycle statistics data to a JSON file."""
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file)

    def update_today_label(self):
        """Updates the label showing the total time worked today."""
        today = datetime.now().strftime('%Y-%m-%d')
        if today in self.data:
            total_minutes = self.data[today] * 15
            hours, minutes = divmod(total_minutes, 60)
            self.today_label.config(text=f"Today: {int(hours)} h {int(minutes)} min")
        else:
            self.today_label.config(text="Today: 0 h 0 min")

    def start_countdown(self):
        """Starts or resumes the countdown timer."""
        if not self.running and not self.paused:
            self.reset_background()
            self.running = True
            self.cycle_count += 1
            self.countdown()
        elif self.paused:
            self.resume_countdown()

    def pause_countdown(self):
        """Pauses the countdown timer if it is running."""
        if self.running:
            self.paused = True
            self.running = False

    def resume_countdown(self):
        """Resumes the countdown timer if it was paused."""
        if self.paused:
            self.paused = False
            self.running = True
            self.countdown()

    def countdown(self):
        """
        The main countdown function. Updates the displayed time
        and window title every second. Changes the background upon completion.
        """
        if self.running and not self.paused:
            mins, secs = divmod(self.remaining, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            self.label.config(text=timeformat)
            self.root.title(timeformat)  # Update window title
            self.remaining -= 1
            if self.remaining < 0:
                self.label.config(text="DONE!!")
                self.root.title("DONE!!")  # Update title on completion
                self.running = False
                self.paused = False
                self.remaining = 900
                self.root.configure(bg='green')
                self.save_cycle_count()
                self.update_today_label()
            else:
                self.root.after(1000, self.countdown)

    def reset_background(self):
        """Resets the window background color to default and resets the title."""
        self.root.configure(bg=self.default_bg)
        self.root.title("15:00")  # Reset title on new start

    def save_cycle_count(self):
        """Saves information about a completed cycle to the statistics."""
        today = datetime.now().strftime('%Y-%m-%d')
        if today in self.data:
            self.data[today] += 1
        else:
            self.data[today] = 1
        self.save_data()
        self.update_today_label()

    def show_statistics(self):
        """Displays a window with the current cycle statistics."""
        stats_text = "Statistics:\n"
        for date, count in self.data.items():
            hours, minutes = divmod(count * 15, 60)
            stats_text += f"{date}: {count} cycles, {int(hours)} h {int(minutes)} min\n"
        messagebox.showinfo("Stats", stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()