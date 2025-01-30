import time
import tkinter as tk
from threading import Thread
from PIL import Image
import pystray
import keyboard

class StopwatchApp:
    def __init__(self):
        self.root = tk.Tk()

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.init_window()

        self.running = False
        self.start_time = 0
        self.last_elapsed = 0
        self.previous_results = []

        self.timer_label = tk.Label(
            self.root, text="00:00:00", font=("Courier", 50, "bold"), fg="lime", bg="black", anchor="e"
        )
        self.timer_label.place(x=self.width, y=0, width=self.width // 2, height=80, anchor="ne")

        self.prev_results_label = tk.Label(
            self.root, text="", font=("Courier", 25, "bold"), fg="lime", bg="black", justify="right"
        )
        self.prev_results_label.place(x=self.width + 380, y=80, width=self.width // 2, anchor="ne")

        self.root.bind("<KeyPress-KP_1>", lambda event: print("KP_1 pressed") or self.start_timer())
        self.root.bind("<KeyPress-KP_2>", lambda event: print("KP_2 pressed") or self.stop_timer())
        self.root.bind("<KeyPress-KP_3>", lambda event: print("KP_3 pressed") or self.reset_timer())

        keyboard.add_hotkey("num 1", self.start_timer)
        keyboard.add_hotkey("num 2", self.stop_timer)
        keyboard.add_hotkey("num 3", self.reset_timer)

        Thread(target=self.create_tray_icon, daemon=True).start()

        self.root.mainloop()

    def init_window(self):
        self.root.title("Секундомер")
        self.root.geometry("250x180+1700+10")
        self.root.attributes("-topmost", True)
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.overrideredirect(True)
        self.root.configure(bg="black")
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.focus_force()  # Принудительно установить фокус на окно

    def update_timer(self):
        while self.running:
            elapsed = time.time() - self.start_time + self.last_elapsed
            minutes, seconds = divmod(int(elapsed), 60)
            milliseconds = int((elapsed - int(elapsed)) * 100)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}:{milliseconds:02}")
            self.root.update()
            time.sleep(0.01)

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.last_elapsed  # Учитываем уже прошедшее время
            Thread(target=self.update_timer, daemon=True).start()

    def stop_timer(self):
        if self.running:
            self.running = False
            self.last_elapsed = time.time() - self.start_time  # Сохраняем прошедшее время

    def reset_timer(self):
        self.running = False
        self.last_elapsed += time.time() - self.start_time
        self.previous_results.insert(0, self.timer_label.cget("text"))
        self.previous_results = self.previous_results[:5]
        self.update_previous_results()
        self.last_elapsed = 0
        self.timer_label.config(text="00:00:00")

    def update_previous_results(self):
        self.prev_results_label.config(text="\n".join(self.previous_results))

    def quit_app(self):
        self.stop_timer()
        self.root.destroy()
        self.icon.stop()

    def create_tray_icon(self):
        icon_image = Image.new("RGB", (64, 64), (0, 0, 0))
        menu = pystray.Menu(
            pystray.MenuItem("Старт", lambda: self.start_timer()),
            pystray.MenuItem("Стоп", lambda: self.stop_timer()),
            pystray.MenuItem("Сброс", lambda: self.reset_timer()),
            pystray.MenuItem("Выход", self.quit_app)
        )
        self.icon = pystray.Icon("Timer", icon_image, "Секундомер", menu)
        self.icon.run()

if __name__ == "__main__":
    StopwatchApp()
