
import iterate_docs
from termcolor import colored
import os
import random

def _clear():
  os.system('cls')

def _launch():

  _clear()
  print(colored('This is the document similarity labeler.', 'green'))

  file_name = input('File name to store data: ')
  start_range = int(input('Document to start at: '))
  end_range = int(input('Number of documents to consider: '))+start_range
  ct = int(input('Number of comparisons: '))

  return (file_name, start_range, end_range, ct)

def _wrap(sstr, width):
  ret = []
  buf = []
  words = sstr.split(' ')
  buf_len = 0

  for word in words:
    if(buf_len+len(word) < width):
      buf_len += len(word)
      buf.append(word)
    else:
      ret.append(' '.join(buf))
      buf = []
      buf_len = 0

  if(buf_len != 0):
    ret.append(' '.join(buf))

  return ret

def _print_lines(lines):
  for line in lines:
    print(line)

def run(TerminalWidth):
  conf = _launch()
  _clear()

  docs = iterate_docs.get_docs()[conf[1] : conf[2]]

  f = open('../../data/test/%s.csv'%(conf[0]), 'w')

  for i in range(conf[3]):

    i1 = random.randint(0, len(docs)-1)
    i2 = random.randint(0, len(docs)-1)

    print(colored("Document 1:", 'green'), end='\r\n\r\n')
    _print_lines(_wrap(docs[i1], TerminalWidth))

    print(colored("Document 2:", 'green'), end='\r\n\r\n')
    _print_lines(_wrap(docs[i2], TerminalWidth))

    sim = None
    try:
      sim = int(input('Similarity (1-10): '))
      f.write('%d, %d, %d\n'%(conf[1]+min(i1,i2), conf[1]+max(i1,i2), sim))
    except:
      pass
    
    _clear()

  f.close()
    
run(160)
