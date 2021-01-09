
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import iterate_docs

def build_model(k):
    return LatentDirichletAllocation(n_components=k)

# returns feature vectors for documents
def update_full_and_extract(model, docs):
   return model.fit_transform(CountVectorizer().fit_transform(docs))

def update(model, docs):
    model.partial_fit(CountVectorizer().fit_transform(docs))

def get_topic_dist(model, doc):
    return model.transform(CountVectorizer().fit_transform(doc))