
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
    return re.sub('[\\W&&\\S]+', '', re.sub('\\s+', ' ', soup.get_text()))

print(compose([_get_text, _get_html], 'http://mudhaniu.x10host.com'))