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
        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        self.url = ""
        self.separator = ","
        self.output_filename = ""
        self.connect_widgets()
        self.refresh_widgets()

    def connect_widgets(self):
        self.url_entry.textChanged.connect(self.url_entry_changed)
        self.clear_button.clicked.connect(self.clear_url)
        self.browse_button.clicked.connect(self.choose_output_filename)
        self.separator_box
        self.insert_button.clicked.connect(self_insert)
        self.cancel_button.clicked.connect(self.close_window)

    def refresh_widgets(self):
        self.refresh_filename_label()
        self.refresh_insert_button()

    def refresh_filename_label(self):
        if not self.output_filename:
            self.output_filename_label.setText("")
        else:
            self.output_filename_label.setText(self.output_filename)
        
    def refresh_insert_button(self):
        if not (self.output_filename and self.url):
            self.insert_button.setEnabled(False)
            self.insert_button.setStyleSheet("background: gray")
        else:
            self.insert_button.setEnabled(True)
            self.insert_button.setStyleSheet("background: lime")

    def url_entry_changed(self, url_entry_string):
        self.url = url_entry_string
        self.refresh_insert_button()

    def clear_url(self):
        """Clears the url"""
        self.url = ""
        self.url_entry.setText("")

    def choose_output_filename(self):
        initial_dir = str(Path.home())
        self.output_filename = QFileDialog.getSaveFileName(
            self,
            "Save File As",
        )[0]
        self.refresh_filename_label()
        self.refresh_insert_button()

    def insert(self):
        word_pairs = self.scrape()
        self.write_to_file(word_pairs)

    def scrape(self):
        """Scrapes the words from the given url"""

        url = "https://app.memrise.com/course/2158097/chemistry-of-rocks-and-minerals/"
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        results = soup.find_all(lambda tag: tag.name == "div" and
                                       tag.get("class") == ["text"])
        it = iter(results)
        for element in it:
            tested_word = element.text
            english_word = next(it).text
            word_pairs.append((tested_word, english_word))
        return word_pairs

    def write_to_file(self, word_pairs):
        with open(self.output_filename) as out_file:
            for pair in word_pairs:
                line = pair[0] + self.separator + pair[1]
                out_file.write(line)

    def close_window(self):
        """Closes the window"""
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemriseScraper()
    window.show()
    app.exec_()
