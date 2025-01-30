import time
import tkinter as tk
from threading import Thread
from PIL import Image
import pystray
import keyboard
from config import Config as cfg

class StopwatchApp:
    def __init__(self):
        self.root = tk.Tk()

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.init_window()

        self.key_bindings = cfg.get_keys()
        self.bind_keys()

        self.running = False
        self.start_time = 0
        self.last_elapsed = 0
        self.previous_results = []

        self.timer_label = tk.Label(
            self.root, text="00:00:00", font=(cfg.get_font(), 50, "bold"), fg="lime", bg="black", anchor="e"
        )
        self.timer_label.place(x=self.width, y=0, width=self.width // 2, height=80, anchor="ne")

        self.prev_results_label = tk.Label(
            self.root, text="", font=(cfg.get_font(), 25, "bold"), fg="lime", bg="black", justify="right"
        )
        self.prev_results_label.place(x=self.width + 380, y=80, width=self.width // 2, anchor="ne")

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
        self.root.focus_force()

    def bind_keys(self):
        keyboard.hook(self.on_key_event)

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.scan_code == self.key_bindings['start_key']:
                self.start_timer()
            elif event.scan_code == self.key_bindings['pause_key']:
                self.pause_timer()
            elif event.scan_code == self.key_bindings['restart_key']:
                self.reset_timer()
            elif event.scan_code == self.key_bindings['delete_key']:
                self.reset_previous()
            elif event.scan_code == self.key_bindings['mark_key']:
                self.mark_timer()

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
            self.start_time = time.time() - self.last_elapsed
            Thread(target=self.update_timer, daemon=True).start()

    def pause_timer(self):
        if self.running:
            self.running = False
            self.last_elapsed = time.time() - self.start_time

    def reset_timer(self):
        if self.timer_label.cget("text") != "00:00:00":
            self.running = False
            self.last_elapsed += time.time() - self.start_time
            self.previous_results.insert(0, self.timer_label.cget("text"))
            self.previous_results = self.previous_results[:15]
            self.update_previous_results()
            self.last_elapsed = 0
            self.timer_label.config(text="00:00:00")

    def mark_timer(self):
        self.previous_results.insert(0, self.timer_label.cget("text"))
        self.previous_results = self.previous_results[:15]
        self.update_previous_results()

    def reset_previous(self):
        self.previous_results = []
        self.update_previous_results()

    def update_previous_results(self):
        self.prev_results_label.config(text="\n".join(self.previous_results))

    def quit_app(self):
        self.pause_timer()
        self.root.destroy()
        self.icon.stop()

    def create_tray_icon(self):
        icon_image = Image.new("RGB", (64, 64), (0, 0, 0))
        menu = pystray.Menu(
            pystray.MenuItem("Старт", lambda: self.start_timer()),
            pystray.MenuItem("Стоп", lambda: self.pause_timer()),
            pystray.MenuItem("Сброс", lambda: self.reset_timer()),
            pystray.MenuItem("Выход", self.quit_app)
        )
        self.icon = pystray.Icon("Timer", icon_image, "Секундомер", menu)
        self.icon.run()

if __name__ == "__main__":
    StopwatchApp()
