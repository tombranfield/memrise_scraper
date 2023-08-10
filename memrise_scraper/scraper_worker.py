"""worker.py"""

import sys
import time
import traceback

from PyQt5.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from memrise_scraper import MemriseScraper


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    error = pyqtSignal()


class ScraperWorker(QRunnable):
    def __init__(self, url, *args, **kwargs):
        super().__init__()
        self.url = url
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        word_pairs = []
        scraper = MemriseScraper(self.url)
        try:
            word_pairs = scraper.scrape()            
        except:
            self.signals.error.emit()
        else:
            self.signals.result.emit(word_pairs)
            self.signals.finished.emit()
