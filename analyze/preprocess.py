
import contractions
import utils
import re
import w2v_model
from gensim.parsing.preprocessing import STOPWORDS
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class Preprocessor(ABC):
  @classmethod
  def make(cls, name):
    if(name == 'entity'):
      return EntityFinder()
    elif(name == 'clean'):
      return TextCleaner() 

  @abstractmethod
  def preprocess(self, text):
    pass

'''
Performs the following operations.

1. Lowercase
2. Contraction expansion
3. Remove all bad characters
4. Stop word removal
5. Out of vocab removal
6. Words of length 1 or 2 characters.
'''
class TextCleaner(Preprocessor):
  NonAlphRegex = re.compile(r'\.|[A-Za-z]+')
  LiteralEscapeRegex = re.compile('\\r|\\n|\\t')
  MinWordLength = 3

  def _remove_escape_chars(self, sstr):
    return re.sub(self.LiteralEscapeRegex, '', sstr)

  def _remove_zero_length_strs(self, tok_stream):
    return filter(lambda tok : not(len(tok) == 0), tok_stream)

  def _tokenize_lowercase(self, sstr):
    return _remove_zero_length_strs(re.split(r'[^A-Za-z\']+', sstr.lower()))

  def _expand_contractions(self, tok_stream):
    return utils.flatmap(lambda tok : contractions.fix(tok).split(' '), tok_stream)

  def _non_alph_removal(self, tok_stream):
    return filter(lambda tok : self.NonAlphRegex.fullmatch(tok), tok_stream)

  def _stop_word_removal(self, tok_stream):
    return filter(lambda tok : not(tok in STOPWORDS), tok_stream)

  def _oov_removal(self, tok_stream):
    return filter(lambda tok : w2v_model.in_corpus(tok), tok_stream)

  def _small_word_removal(self, tok_stream):
    return filter(lambda tok : len(tok) >= self.MinWordLength, tok_stream)

  def preprocess(self, doc):
    return list(utils.compose([
      _remove_escape_chars,
      _tokenize_lowercase, 
      _expand_contractions,
      _non_alph_removal,
      _stop_word_removal,
      _oov_removal,
      _small_word_removal
    ], doc))

class EntityFinder(Preprocessor):
  RGX = re.compile(r'(([A-Z][a-z]+\s*)+)')

  def preprocess(txt):
    return [match.group().lower() for match in RGX.finditer(txt)]
