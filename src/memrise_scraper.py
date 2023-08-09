"""memrise_scraper.py"""


class MemriseScraper:
    """Scraps data from a Memrise course page"""
    def __init__(self, url):
        self.url = url
        self.clean_url()

    def scrape_pages(self):
        """Attempts scrapes on course homepage and subsequent pages"""
        url = self.clean_url()
        try:
            self.scrape_individual_page(url)
        except ValueError:
            raise ValueError
        else:
            if len(self.word_pairs) > 0: 
                return  
            current_page = 1
            while True:
                new_url = url + "/" + str(current_page) + "/"
                num_words_before = len(self.word_pairs)
                self.scrape_individual_page(new_url)
                num_words_after = len(self.word_pairs)
                if num_words_before == num_words_after:
                    return
                print("Scraping page", current_page)
                msg = "Scraping page " + str(current_page)
                self.status_label.setText(msg)
                current_page += 1

    def scrape_individual_page(self, url):
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
            it = iter(results)
            for element in it:
                tested_word = element.text
                english_word = next(it).text
                self.word_pairs.append((tested_word, english_word))
