
import spacy

def init():
    return spacy.load('en_core_web_sm')

# try using BERT
def process(nlp, doc):
    data = nlp(doc)
    return data

process(init(), "the quick brown fox jumped over the lazy dog.")