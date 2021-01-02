
import db_interface
import requests
from bs4 import BeautifulSoup
from utils import *
import re

def _get_html(url):
    req = requests.get(url)
    return req.text if req.status_code == 200 else None

def _get_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    return re.sub(r'[^\\,\\.A-Za-z ]+', '', re.sub(r'\\s+', ' ', soup.get_text()))

def get_text(url):
    return compose([_get_text, _get_html], url)