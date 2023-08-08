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
        self.url = ""
        self.separator = ","
        self.out_filename = ""
        self.connect_widgets()

    def connect_widgets(self):
        self.url_entry.textChanged.connect(self.url_entry_changed)
        self.clear_button.clicked.connect(self.clear_url)
#        self.browse_button
#        self.output_filename_label
#        self.separator_box


    def url_entry_changed(self, url_entry_string):
        self.url = url_entry_string
        print(self.url)

    def clear_url(self):
        """Clears the url"""
        print("clearing")
        self.url = ""
        self.url_entry.setText("")

    def scrape(self):
        """Scrapes the words from the given url"""

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
