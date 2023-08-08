"""memrise_scraper.py"""


from bs4 import BeautifulSoup
from urllib.request import urlopen

# Will provide a means to enter a URL later... for now, just testing
url = "https://app.memrise.com/course/2158097/chemistry-of-rocks-and-minerals/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

results = soup.find_all(lambda tag: tag.name == "div" and
                                    tag.get("class") == ["text"])

it = iter(results)
for element in it:
    print(element.text, next(it).text)
