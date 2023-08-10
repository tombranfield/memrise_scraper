"""memrise_scraper.py"""


from urllib.request import urlopen

from bs4 import BeautifulSoup


class MemriseScraper:
    """Scraps data from a Memrise course page"""
    def __init__(self, url):
        self.url = url

    def scrape(self):
        """Attempts scrapes on course homepage and subsequent pages"""
        word_pairs = []
        url = self._clean_url(self.url)
        try:
            word_pairs.extend(self._scrape_individual_page(url))
        except ValueError:
            raise ValueError
        else:
            if len(word_pairs) > 0:
                return word_pairs
            current_page = 1
            while True:
                new_url = url + "/" + str(current_page) + "/"
                num_words_before = len(word_pairs)
                word_pairs.extend(self._scrape_individual_page(new_url))
                num_words_after = len(word_pairs)
                if num_words_before == num_words_after:
                    return word_pairs
                current_page += 1

    def _scrape_individual_page(self, url):
        """Scrapes the words from the given url"""
        try:
            page = urlopen(url)
        except ValueError:
            raise ValueError
        else:
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            results = soup.find_all(lambda tag: tag.name == "div" and
                                       tag.get("class") == ["text"])
            word_pairs = []
            results_iterable = iter(results)
            for element in results_iterable:
                tested_word = element.text
                english_word = next(results_iterable).text
                word_pairs.append((tested_word, english_word))
            return word_pairs

    def _clean_url(self, url):
        """Returns a url string without an ending slash"""
        if url[-1] == "/":
            return url[:-1]
        return url
