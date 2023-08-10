"""main.py"""

import os

from pathlib import Path


def run():
    MAIN_PATH = str(Path(__file__).parents[0] / "memrise_scraper" / "main_window.py")
    os.system(f"python {MAIN_PATH}")


if __name__ == "__main__":
    run()
