"""memrise_scraper.py"""


from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlopen
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QMainWindow,
    QMessageBox,
)


class MemriseScraper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "memrise_scraper.ui"), self)
        self.url = ""
        self.separator = ","
        self.output_filename = ""
        self.connect_widgets()
        self.refresh_widgets()

    def connect_widgets(self):
        self.url_entry.textChanged.connect(self.url_entry_changed)
        self.clear_button.clicked.connect(self.clear_url)
        self.browse_button.clicked.connect(self.choose_output_filename)
#        self.separator_box

    def refresh_widgets(self):
        self.refresh_filename_label()

    def refresh_filename_label(self):
        if not self.output_filename:
            self.output_filename_label.setText("")
        else:
            self.output_filename_label.setText(self.output_filename)

    def url_entry_changed(self, url_entry_string):
        self.url = url_entry_string
        print(self.url)

    def clear_url(self):
        """Clears the url"""
        print("clearing")
        self.url = ""
        self.url_entry.setText("")

    def choose_output_filename(self):
        initial_dir = str(Path.home())
        self.output_filename = QFileDialog.getSaveFileName(
            self,
            "Save File As",
        )[0]
        self.refresh_filename_label()

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
