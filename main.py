import tkinter as tk
from tkinter import filedialog, messagebox
import json
import threading
import ctypes
import os
from pynput import keyboard
from recorder import Recorder
from playback import play_file

# Constants for Windows HWND management
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Click Automator Pro")
        self.root.geometry("400x620")
        
        # Enable Always-on-Top
        self.root.attributes("-topmost", True)
        self.force_window_on_top()
        
        self.recorder = Recorder()
        self.selected_path = None
        self.is_playing = False
        self.stop_playback_event = threading.Event()
        self.speed = 1.0
        self.latest_data = []

        # --- Status Label ---
        self.status_label = tk.Label(root, text="Status: Idle", fg="blue", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)

        # --- Recording Controls ---
        tk.Label(root, text="--- RECORDING ---", font=("Arial", 9, "bold")).pack()
        self.btn_start_rec = tk.Button(root, text="Start Recording", width=30, command=self.start_rec, bg="#28a745", fg="white")
        self.btn_start_rec.pack(pady=2)
        self.btn_stop_rec = tk.Button(root, text="Stop Recording", width=30, command=self.stop_rec, bg="#dc3545", fg="white", state="disabled")
        self.btn_stop_rec.pack(pady=2)

        # --- Speed Controls ---
        tk.Label(root, text="\n--- SPEED CONTROL ---", font=("Arial", 9, "bold")).pack()
        sf = tk.Frame(root); sf.pack()
        tk.Button(sf, text="-", width=4, command=self.speed_down).pack(side="left")
        self.speed_label = tk.Label(sf, text="1.0x", width=8, font=("Arial", 10, "bold"))
        self.speed_label.pack(side="left")
        tk.Button(sf, text="+", width=4, command=self.speed_up).pack(side="left")

        # --- Loop Settings ---
        tk.Label(root, text="\n--- REPEAT COUNT (0=∞) ---", font=("Arial", 9, "bold")).pack()
        self.repeat_entry = tk.Entry(root, width=10, justify='center')
        self.repeat_entry.insert(0, "1")
        self.repeat_entry.pack(pady=5)

        # --- Automation Playback ---
        tk.Label(root, text="\n--- AUTOMATION (Ctrl+X to Play/Stop) ---", font=("Arial", 9, "bold")).pack()
        tk.Button(root, text="1. Select JSON File", width=30, command=self.select_file).pack(pady=2)
        self.btn_play = tk.Button(root, text="2. Play/Stop (Ctrl+X)", width=30, command=self.toggle_playback, bg="#007bff", fg="white")
        self.btn_play.pack(pady=10)
        tk.Button(root, text="Save Latest Recording", width=30, command=self.save_rec).pack()

        # Global Hotkey Listener (Ctrl + X)
        self.hotkey = keyboard.GlobalHotKeys({'<ctrl>+x': self.toggle_playback})
        self.hotkey.daemon = True
        self.hotkey.start()

        # Keep pinned to front every 2 seconds
        self.keep_pinned()

    def force_window_on_top(self):
        """Native Windows pinning to stay over full-screen apps"""
        if os.name == 'nt': 
            try:
                hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
                ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            except:
                pass

    def keep_pinned(self):
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(2000, self.keep_pinned)

    def speed_up(self):
        if self.speed < 10.0: self.speed = round(self.speed + 0.5, 1); self.speed_label.config(text=f"{self.speed}x")

    def speed_down(self):
        if self.speed > 0.5: self.speed = round(self.speed - 0.5, 1); self.speed_label.config(text=f"{self.speed}x")

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.selected_path = path
            self.status_label.config(text="File Loaded", fg="green")

    def toggle_playback(self):
        if not self.is_playing:
            if not self.selected_path:
                return 
            self.start_playback()
        else:
            self.stop_playback()

    def start_playback(self):
        try: rep = int(self.repeat_entry.get())
        except: rep = 1
        self.is_playing = True
        self.stop_playback_event.clear()
        self.status_label.config(text="Status: PLAYING...", fg="green")
        threading.Thread(target=self.run_play, args=(self.selected_path, rep, self.speed), daemon=True).start()

    def run_play(self, p, r, s):
        play_file(p, r, s, self.stop_playback_event)
        self.is_playing = False
        self.root.after(0, lambda: self.status_label.config(text="Status: Idle", fg="blue"))

    def stop_playback(self):
        self.stop_playback_event.set()
        self.is_playing = False
        self.status_label.config(text="Status: Stopped", fg="red")

    def start_rec(self):
        self.recorder.start()
        self.status_label.config(text="Status: RECORDING...", fg="red")
        self.btn_start_rec.config(state="disabled"); self.btn_stop_rec.config(state="normal")

    def stop_rec(self):
        self.latest_data = self.recorder.stop()
        self.status_label.config(text="Status: Recorded", fg="blue")
        self.btn_start_rec.config(state="normal"); self.btn_stop_rec.config(state="disabled")

    def save_rec(self):
        p = filedialog.asksaveasfilename(defaultextension=".json")
        if p:
            with open(p, 'w') as f: json.dump(self.latest_data, f)

if __name__ == "__main__":
    root = tk.Tk(); app = AutoClickerGUI(root); root.mainloop()