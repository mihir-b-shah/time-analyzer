
from bs4 import BeautifulSoup
import re
import json

def get_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return re.sub(r'[^\\,\\.A-Za-z ]+', '', re.sub(r'\\s+', ' ', soup.get_text()))

def get_docs(file_num):
    jsn = json.load(open('../../../data/pages%d.txt'%(file_num), "r", errors="ignore"))
    return list(map(get_text, jsn))