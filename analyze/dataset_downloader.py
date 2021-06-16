
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import gensim.downloader as api
from gensim.test.utils import get_tmpfile

def download_w2v_model():
  model = api.load('glove-wiki-gigaword-300')
  model.save('models/vectors.kv')

def download_d2v_model():
  corpus = api.load('semeval-2016-2017-task3-subtaskA-unannotated')
  documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(corpus)]
  model = Doc2Vec(documents, workers=4, min_count=1)
  model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
  model.save('models/data/d2v.model')

download_d2v_model()
