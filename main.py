import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("15:00 Таймер")
        
        # Настройки окна
        self.root.attributes("-topmost", True)  # Всегда поверх других окон
        self.root.overrideredirect(True)  # Убираем рамку окна
        self.root.geometry("150x60+20+20")  # Ширина x Высота + X + Y позиция
        self.root.configure(bg="black")  # Черный фон
        
        # Прозрачность (если поддерживается)
        try:
            self.root.wm_attributes("-alpha", 0.85)  # 85% прозрачности
        except:
            pass
        
        # Текст таймера
        self.label = tk.Label(
            root, 
            text="15:00", 
            font=("Arial", 24, "bold"), 
            fg="white", 
            bg="black"
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Обработка кликов
        self.label.bind("<Button-1>", self.toggle_timer)  # ЛКМ - старт/пауза
        self.label.bind("<Button-3>", self.show_menu)     # ПКМ - меню

        # Перетаскивание окна
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)
        
        # Настройки таймера
        self.total_seconds = 900  # 15 минут
        self.remaining = self.total_seconds
        self.running = False
        self.data_file = "countdown_data_15.json"  # Имя файла 
        self.load_data()
        
        # Запуск обновления
        self.update_timer()

    def toggle_timer(self, event=None):
        """Старт/пауза по клику"""
        self.running = not self.running
        if self.running and self.remaining <= 0:
            self.remaining = self.total_seconds  # Сброс, если время вышло
        if self.running:
            self.root.after(1000, self.update_timer)

    def update_timer(self):
        """Обновляет таймер каждую секунду"""
        if self.running and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining <= 0:
            self.label.config(text="ГОТОВО!", fg="white")
            self.running = False
            self.save_cycle()
            self.root.bell()  # Звуковой сигнал
        else:
            # Если на паузе, отображаем текущее значение
            mins, secs = divmod(self.remaining, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")

    def show_menu(self, event=None):
        """Контекстное меню по ПКМ"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Сброс", command=self.reset_timer)
        menu.add_command(label="Статистика", command=self.show_stats)
        menu.add_command(label="Выход", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)
        menu.grab_release()

    def reset_timer(self):
        """Сброс таймера"""
        self.running = False
        self.remaining = self.total_seconds
        self.label.config(text="15:00", fg="white")
        self.update_timer()

    def load_data(self):
        """Загружает статистику"""
        try:
            with open(self.data_file, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    def save_cycle(self):
        """Сохраняет завершенный цикл"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.data[today] = self.data.get(today, 0) + 1
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def show_stats(self):
        """Показывает статистику"""
        stats = []
        for date, count in self.data.items():
            total_min = count * 15
            hours, mins = divmod(total_min, 60)
            stats.append(f"{date}: {count} циклов ({hours} ч {mins} мин)")
        
        message = "\n".join(stats) if stats else "Нет данных"
        messagebox.showinfo("Статистика", message)

    # === Перетаскивание окна ===
    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
