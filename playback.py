import time
import json
from pynput import mouse, keyboard

def play_file(filepath, repeat_count, speed_factor, stop_event):
    mouse_ctrl = mouse.Controller()
    kb_ctrl = keyboard.Controller()

    try:
        with open(filepath, 'r') as f:
            events = json.load(f)
    except:
        return

    iterations = 0
    while True:
        # 0 in repeat_count means infinite loop
        if repeat_count != 0 and iterations >= repeat_count:
            break
            
        last_time = 0
        for event in events:
            if stop_event.is_set():
                return

            # Speed calculation: Dividing the original delay by speed factor
            original_delay = event['time'] - last_time
            adjusted_delay = original_delay / speed_factor
            
            time.sleep(max(0, adjusted_delay))
            last_time = event['time']

            if event['type'] == 'mouse_click':
                mouse_ctrl.position = (event['x'], event['y'])
                btn = mouse.Button.left if 'left' in event['button'] else mouse.Button.right
                mouse_ctrl.click(btn)
            
            elif event['type'] == 'key_press':
                try:
                    if event['key'].startswith('Key.'):
                        key_attr = event['key'].split('.')[1]
                        key_to_use = getattr(keyboard.Key, key_attr)
                    else:
                        key_to_use = event['key']
                    kb_ctrl.press(key_to_use)
                    kb_ctrl.release(key_to_use)
                except:
                    pass
        iterations += 1