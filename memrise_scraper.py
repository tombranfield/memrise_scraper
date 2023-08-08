"""memrise_scraper.py"""


from bs4 import BeautifulSoup
from urllib.request import urlopen

# Want to choose URL

# Want to choose seperator (for output file)
# Choose output file name and location

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
