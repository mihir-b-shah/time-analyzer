
from sklearn.decomposition import PCA, TruncatedSVD, SparsePCA
from sklearn.feature_extraction.text import CountVectorizer
from mpl_toolkits import mplot3d 
from matplotlib import pyplot as plt

import d2v_model
import iterate_docs
import numpy as np
from itertools import accumulate

def get_pca(docs):
  pca = PCA(n_components=3)
  d2vm = d2v_model.get_d2v_model()
  ret = pca.fit_transform([d2vm.infer_vector(doc.split(' ')) for doc in docs])
  return ret, list(accumulate(pca.explained_variance_ratio_))

def get_tsvd(docs):
  tsvd = TruncatedSVD(n_components=3)
  cts = CountVectorizer().fit_transform(docs)
  ret = tsvd.fit_transform(cts)
  return ret, list(accumulate(tsvd.explained_variance_ratio_))

def plot_points(dim_red_func, docs):
  points, freq_ = dim_red_func(docs)
  print('total variance preserved: ' + str(freq_))

  fig = plt.figure()
  ax = plt.axes(projection ='3d')
  dim_tuples = [(min(points.T[i])-1, max(points.T[i])+1) for i in range(3)]

  ax.set_xlim(*dim_tuples[0])
  ax.set_ylim(*dim_tuples[1])
  ax.set_zlim(*dim_tuples[2])
  
  print(dim_tuples)
  ax.scatter3D(points.T[0], points.T[1], points.T[2], cmap ='black') 
  plt.show()

print(get_pca(iterate_docs.get_docs()[0:40])[1])
print(get_tsvd(iterate_docs.get_docs()[0:40])[1])
