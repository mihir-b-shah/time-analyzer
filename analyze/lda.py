from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

def build_model(k):
    return LatentDirichletAllocation(n_components=k)

def update(model, docs):
    model.partial_fit(CountVectorizer().fit_transform(docs))

def get_topic_dist(model, doc):
    return model.transform(CountVectorizer().fit_transform(doc))