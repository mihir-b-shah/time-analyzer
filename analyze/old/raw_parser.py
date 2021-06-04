
from bs4 import BeautifulSoup
import re
import json
import os
import pickle
import clean_text

def get_text(html):
  soup = BeautifulSoup(html, 'html.parser')

  for item in (soup.select('script') + soup.select('style')):
    item.decompose()
    
  return clean_text.clean(soup.get_text())

def get_docs(file_num):
  jsn = json.load(open('../../data/pages/pages%d.txt'%(file_num), "r", errors="ignore"))
  return list(map(get_text, jsn))

def extract_file_num(fname):
  return int(fname[fname.index('pages')+len('pages'):-len('.txt')])

def persist():
  for fname in os.listdir('../../data/pages'):
    file_num = extract_file_num(fname) 
    print('file %d completed'%(file_num))
    with open('../../data/docs/docs%d.data'%(file_num), 'wb') as out_file:
      pickle.dump(get_docs(file_num), out_file)

# persist()
