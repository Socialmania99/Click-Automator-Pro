import time
from pynput import mouse, keyboard

class Recorder:
    def __init__(self):
        self.events = []
        self.start_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.is_recording = False

    def on_click(self, x, y, button, pressed):
        if pressed and self.is_recording:
            self.events.append({
                'type': 'mouse_click',
                'x': x, 'y': y,
                'button': str(button),
                'time': time.time() - self.start_time
            })

    def on_press(self, key):
        if self.is_recording:
            try:
                k = key.char
            except AttributeError:
                k = str(key)
            self.events.append({
                'type': 'key_press',
                'key': k,
                'time': time.time() - self.start_time
            })

    def start(self):
        self.events = []
        self.is_recording = True
        self.start_time = time.time()
        self.mouse_listener = mouse.Listener(on_click=self.on_click, daemon=True)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, daemon=True)
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        self.is_recording = False
        if self.mouse_listener: self.mouse_listener.stop()
        if self.keyboard_listener: self.keyboard_listener.stop()
        return self.events