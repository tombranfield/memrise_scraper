"""memrise_scraper.py"""


from bs4 import BeautifulSoup
from urllib.request import urlopen

url = https://app.memrise.com/course/2158097/chemistry-of-rocks-and-minerals/
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

