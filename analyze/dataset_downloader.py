import gensim.downloader as api

model = api.load('glove-wiki-gigaword-300')
model.save('../../../data/vectors.kv')