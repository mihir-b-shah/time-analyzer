
from bs4 import BeautifulSoup

def html_to_text(html):
  soup = BeautifulSoup(html, 'html.parser')
  for item in (soup.select('script') + soup.select('style')):
    item.decompose()
  return soup.get_text()
