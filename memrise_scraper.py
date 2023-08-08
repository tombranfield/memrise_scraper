"""memrise_scraper.py"""


from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlopen
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MemriseScraper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "memrise_scraper.ui"), self)


        url = "https://app.memrise.com/course/2158097/chemistry-of-rocks-and-minerals/"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find_all(lambda tag: tag.name == "div" and
                                       tag.get("class") == ["text"])

        word_pairs = []


        it = iter(results)
        for element in it:
            tested_word = element.text
            english_word = next(it).text
            word_pairs.append((tested_word, english_word))

            print(word_pairs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemriseScraper()
    window.show()
    app.exec_()
