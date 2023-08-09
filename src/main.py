"""main.py"""

import os

from pathlib import Path


FILE_PATH = str(Path(__file__).parents[1] / "gui" / "main_window.py")

os.system(f"python {FILE_PATH}")
