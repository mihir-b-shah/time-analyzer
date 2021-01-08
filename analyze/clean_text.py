
import contractions
import utils
import re
import glove_model
from gensim.parsing.preprocessing import STOPWORDS

'''
Performs the following operations.

1. Lowercase
2. Contraction expansion
3. Remove all bad characters
4. Stop word removal
5. Out of vocab removal
----------------------------------------
6. Stemming (too inaccurate)
7. Coreference (nice but too expensive)

'''

vocab = glove_model.get_w2v_model().wv.vocab
NonAlphRegex = re.compile(r'\.|[A-Za-z]+')
LiteralEscapeRegex = re.compile('\\r|\\n|\\t')

def remove_escape_chars(sstr):
    return re.sub(LiteralEscapeRegex, '', sstr)

def _remove_zero_length_strs(tok_stream):
    return filter(lambda tok : not(len(tok) == 0), tok_stream)

def tokenize_lowercase(sstr):
    return _remove_zero_length_strs(re.split(r'[^A-Za-z\']+', sstr.lower()))

def expand_contractions(tok_stream):
    return utils.flatmap(lambda tok : contractions.fix(tok).split(' '), tok_stream)

def non_alph_removal(tok_stream):
    return filter(lambda tok : NonAlphRegex.fullmatch(tok), tok_stream)

def stop_word_removal(tok_stream):
    return filter(lambda tok : not(tok in STOPWORDS), tok_stream)

def oov_removal(tok_stream):
    return filter(lambda tok : tok in vocab, tok_stream)

def clean(doc):
    return ' '.join(list(utils.compose([
        remove_escape_chars,
        tokenize_lowercase, 
        expand_contractions,
        non_alph_removal,
        stop_word_removal,
        oov_removal
    ], doc)))