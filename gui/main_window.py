"""main.py"""


from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import urlopen
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThreadPool

from PyQt5.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QMainWindow,
    QMessageBox,
)

from src.file_writer import FileWriter
from src.memrise_scraper import MemriseScraper

from gui.scraper_worker import ScraperWorker


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[1] / "gui" / "main_window.ui"), self)
        self.setStyleSheet(open( str(Path(__file__).parents[1] / "gui" / "stylesheet.css")) .read())
        self.url = ""
        self.output_filename = ""
        self.word_pairs = []
        self.setup_widgets()
        self.refresh_widgets()
        self.threadpool = QThreadPool()

    def setup_widgets(self):
        self.separator = self.separator_box.currentText()
        self.status_label.setText("")
        self.url_entry.textChanged.connect(self.url_entry_changed)
        self.clear_button.clicked.connect(self.clear_url_box)
        self.browse_button.clicked.connect(self.choose_output_filename)
        self.separator_box.currentTextChanged.connect(self.separator_changed)
        self.insert_button.clicked.connect(self.insert)
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

    def clear_url_box(self):
        """Clears the url"""
        self.url = ""
        self.url_entry.setText("")

    def separator_changed(self, separator):
        self.separator = separator

    def disable_buttons(self):
        self.insert_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.url_entry.setEnabled(False)
        self.separator_box.setEnabled(False)

    def enable_buttons(self):
        self.insert_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.url_entry.setEnabled(True)
        self.separator_box.setEnabled(True)

    def reset(self):
        self.clear_url_box()
        self.output_filename = ""
        self.refresh_filename_label()
        self.refresh_insert_button()
        self.separator_box.setCurrentIndex(0)
        self.word_pairs = []
        self.status_label.setText("")

    def choose_output_filename(self):
        initial_dir = str(Path.home())
        self.output_filename = QFileDialog.getSaveFileName(
            self,
            "Save File As",
        )[0]
        self.refresh_filename_label()
        self.refresh_insert_button()

    """
    def insert(self):
        if self.url and self.output_filename:
            try:
                self.scrape()
                print("after self.scrape()")
            except ValueError:
                self.unsuccessful_message_box()    
            else:
                self.write_to_file()
                self.successful_message_box()
            finally: 
                self.reset()
    """

    def insert(self):
        if self.url and self.output_filename:
            self.status_label.setText("Scraping...")
            self.disable_buttons()
            self.scrape()

    def scrape(self):
        """Attempts scrapes on course homepage and subsequent pages"""
        scraper_worker = ScraperWorker(self.url)
        scraper_worker.signals.result.connect(self.got_result)
        scraper_worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(scraper_worker)

    def got_result(self, s):
        self.word_pairs = s

    def thread_complete(self):
        print("THREAD COMPLETE")
        self.status_label.setText("")
        self.write_to_file()
        self.reset()
        self.enable_buttons()
        self.successful_message_box()

    def write_to_file(self):
        file_writer = FileWriter(self.word_pairs, self.separator, self.output_filename)
        file_writer.write_to_file() 

    def close_window(self):
        """Closes the window"""
        self.close()

    def clean_url(self):
        """Returns a url without an ending slash"""
        if self.url[-1] == "/":
            return self.url[:-1]
        return self.url

    def message_box(self, title: str, message: str):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        button = dlg.exec_()

    def successful_message_box(self):
        title = "Success"
        message = "Words inserted successfully"
        self.message_box(title, message)

    def unsuccessful_message_box(self):
        title =  "Error"
        message = "Scraping failed. Please check the URL"
        self.message_box(title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()
