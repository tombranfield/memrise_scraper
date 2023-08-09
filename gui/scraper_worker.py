"""worker.py"""


import traceback

from PyQt5.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from src.memrise_scraper import MemriseScraper


class WorkerSignals(QObject):
    result = pyqtSignal(object)
    finished = pyqtSignal()
    error = pyQtSignal(tuple)


class ScraperWorker(QRunnable):
    def __init__(self, url, *args, **kwargs):
        super().__init__()
        self.url = url
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


    @pyqtSlot()
    def run(self):
        try:
            """
            result = self.fn(*self.args, **self.kwargs)
            """
            scraper = MemriseScraper(self.url)
            word_pairs = scraper.scrape()
        except:
            traceback.print_exc()
            exctype, value = sys.exc.info()[:2]
            self.signals.error.emit(
                (exctype, value, traceback.format_exc())
            )
        else:
            self.signals.result.emit(word_pairs)
        finally:
            self.signals.finished.emit()
