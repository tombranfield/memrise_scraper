"""worker.py"""


from PyQt5.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from memrise_scraper import MemriseScraper


class WorkerSignals(QObject):
    """Signals for the worker"""
    result = pyqtSignal(object)
    finished = pyqtSignal()
    error = pyqtSignal()


class ScraperWorker(QRunnable):
    """A worker that handles scraping"""
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
