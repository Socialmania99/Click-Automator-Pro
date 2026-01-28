🖱️ Click Automator Pro

Click Automator Pro is a high-performance Python-based automation utility designed to record complex mouse and keyboard sequences and play them back with precision. It features a modern GUI that stays pinned on top of other applications, making it ideal for gaming, repetitive data entry, and workflow automation.


✨ Features

Dual-Input Recording: Captures both mouse movements/clicks and keyboard strokes simultaneously.

Speed Control: Adjustable playback speed from 0.5x (slow-motion) up to 10.0x (ultra-fast).

Intelligent Looping: Set a specific repeat count or use 0 for infinite loops.

Global Hotkey: Use Ctrl + X to instantly start or stop the automation from anywhere.

Super-Pinning: Stays on top of other windows (even high-priority apps) using native Windows API.

Portable Storage: Save and load your automation sequences as lightweight .json files.


🚀 Getting Started

Installation

If you are running the source code, install the required dependencies:

Bash
pip install pynput


How to Use
Record: Click Start Recording, perform your actions, then click Stop Recording.

Save: Click Save Latest Recording to name and store your automation.

Load: Click Select JSON File to choose a sequence for playback.

Execute: Press Ctrl + X to start the playback. Press Ctrl + X again to stop it immediately.


🛠️ Technical Details

Language: Python 3.x

Libraries: tkinter (UI), pynput (Input Control), threading (Non-blocking execution).

Binary Build: Compiled using PyInstaller.

Platform: Optimized for Windows (includes ctypes for user32.dll window management).


📦 Building the Executable

To create your own standalone .exe, run the following command in your Windows terminal:

Bash
pyinstaller --noconfirm --onefile --windowed --name "ClickAutomator_Pro" --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" --hidden-import "pynput.platforms.common" main.py


⚠️ Safety & Requirements

Administrator Rights: For the clicker to work inside games or system tools (like Task Manager), right-click the .exe and select Run as Administrator.

Windowed Mode: Always-on-top works best when games are in Windowed or Borderless Windowed mode.

Security: Some antivirus software may flag the app because it "hooks" into mouse and keyboard inputs. This is a false positive; you may need to add an exclusion.



📜 License
This project is open-source and available under the MIT License.