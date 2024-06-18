import menu_ui

import platform
import ctypes

# Fixes resolution scaling issue on Windows.
if platform.system() == "Windows":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

menu_ui.start_game()
