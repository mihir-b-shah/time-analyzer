
from bs4 import BeautifulSoup
import re
import json

def get_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    for item in (soup.select('script') + soup.select('style')):
        item.decompose()

    return re.sub('\.+', '.', re.sub(r'\s+', ' ', 
            re.sub(r'[^\.A-Za-z ]+', ' ', soup.get_text().lower())))

def get_docs(file_num):
    jsn = json.load(open('../../../data/pages%d.txt'%(file_num), "r", errors="ignore"))
    return list(map(get_text, jsn))

print(get_docs(12)[1])