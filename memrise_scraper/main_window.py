"""main.py"""


import os
from pathlib import Path
import random
import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import (
    QThreadPool,
    QTimer,
)

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from file_writer import FileWriter
from memrise_scraper import MemriseScraper
from scraper_worker import ScraperWorker


class Main(QMainWindow):
    """The Main Window for the Memrise Scraper program"""
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "main_window.ui"), self)
        self.setStyleSheet(open( str(Path(__file__).parents[0] / "stylesheet.css")) .read())
        self.url = ""
        self.output_filename = ""
        self.word_pairs = []
        self.setup_widgets()
        self.refresh_widgets()
        self.threadpool = QThreadPool()
        self.is_scraping = False
        self.setup_timer()

    def setup_timer(self):
        """Sets up, connects, and starts the timer"""
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_status_label)
        self.timer.start()

    def setup_widgets(self):
        """Setup up the widgets for their initial state and connections"""
        self.separator = self.separator_box.currentText()
        self.status_label.setText("")
        self.url_entry.textChanged.connect(self.url_entry_changed)
        self.clear_button.clicked.connect(self.clear_url_box)
        self.browse_button.clicked.connect(self.choose_output_filename)
        self.separator_box.currentTextChanged.connect(self.separator_changed)
        self.insert_button.clicked.connect(self.insert)
        self.cancel_button.clicked.connect(self.close_window)

    def refresh_widgets(self):
        """Refresh display widgets so they show correct information"""
        self.refresh_filename_label()
        self.refresh_insert_button()

    def refresh_filename_label(self):
        """Refresh the displayed filename"""
        if not self.output_filename:
            self.output_filename_label.setText("")
        else:
            self.output_filename_label.setText(self.output_filename)

    def refresh_insert_button(self):
        """Sets the insert button according to whether insertion can happen"""
        if not (self.output_filename and self.url):
            self.insert_button.setEnabled(False)
            self.insert_button.setStyleSheet("background: gray")
        else:
            self.insert_button.setEnabled(True)
            self.insert_button.setStyleSheet("background: lime")

    def url_entry_changed(self, url_entry_string):
        """Updates the url attribute when the lineEdit entry is changed"""
        self.url = url_entry_string
        self.refresh_insert_button()

    def clear_url_box(self):
        """Clears the url and the displayed url"""
        self.url = ""
        self.url_entry.setText("")

    def separator_changed(self, separator):
        """Updates the separator attribute when the combobox is changed"""
        self.separator = separator

    def disable_buttons(self):
        """Disables all buttons and boxes, for when scraping is taking place"""
        self.insert_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.clear_button.setEnabled(False)
        self.url_entry.setEnabled(False)
        self.separator_box.setEnabled(False)

    def enable_buttons(self):
        """Re-enables all buttons and boxes"""
        self.insert_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.clear_button.setEnabled(True)
        self.url_entry.setEnabled(True)
        self.separator_box.setEnabled(True)

    def reset(self):
        """Resets all attributes and display widgets"""
        self.enable_buttons()
        self.clear_url_box()
        self.output_filename = ""
        self.refresh_filename_label()
        self.refresh_insert_button()
        self.separator_box.setCurrentIndex(0)
        self.word_pairs = []
        self.status = ""

    def choose_output_filename(self):
        """Prompts the user to choose a filename to save to"""
        self.output_filename = QFileDialog.getSaveFileName(
            self,
            "Save File As",
        )[0]
        self.refresh_filename_label()
        self.refresh_insert_button()

    def insert(self):
        """Starts scraping"""
        if self.url and self.output_filename:
            self.is_scraping = True
            self.disable_buttons()
            self.scrape()

    def scrape(self):
        """Attempts scrapes on course homepage and subsequent pages"""
        scraper_worker = ScraperWorker(self.url)
        scraper_worker.signals.result.connect(self.scraper_result)
        scraper_worker.signals.finished.connect(self.thread_complete)
        scraper_worker.signals.error.connect(self.scraper_error)
        self.threadpool.start(scraper_worker)

    def scraper_result(self, s):
        """Takes result from the scraper worker"""
        self.word_pairs = s

    def thread_complete(self):
        """Takes finish signal from the scraper worker"""
        self.is_scraping = False
        self.write_to_file()
        self.reset()
        self.enable_buttons()
        self.successful_message_box()

    def scraper_error(self):
        """Takes error signal from the scraper worker"""
        self.is_scraping = False
        self.reset()
        self.unsuccessful_message_box()
        self.enable_buttons()

    def update_status_label(self):
        """Updates the status label on whether scraping is taking place"""
        if self.is_scraping:
            r = random.randint(1, 4)
            msg = r * "." + "Scraping" + (r + 1) * "."
            self.status_label.setText(msg)
        else:
            self.status_label.setText("")

    def write_to_file(self):
        """Writes the word pairs to file"""
        file_writer = FileWriter(self.word_pairs, self.separator, self.output_filename)
        file_writer.write_to_file()

    def close_window(self):
        """Closes the window"""
        os._exit(1)

    def clean_url(self):
        """Returns a url without an ending slash"""
        if self.url[-1] == "/":
            return self.url[:-1]
        return self.url

    def message_box(self, title: str, message: str):
        """A generic message box that takes a given title and message"""
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
