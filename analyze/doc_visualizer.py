
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from mpl_toolkits import mplot3d 
from matplotlib import pyplot as plt

import gensim_model
import iterate_docs
import numpy as np

def get_pca(docs):
    pca = PCA(n_components=3)
    d2v_model = gensim_model.get_d2v_model()

    ret = pca.fit_transform([d2v_model.infer_vector(doc.split(' ')) for doc in docs])
    return ret, sum(pca.explained_variance_ratio_)

def get_tsvd(docs):
    tsvd = TruncatedSVD(n_components=3)
    cts = CountVectorizer().fit_transform(docs)

    ret = tsvd.fit_transform(cts)
    return ret, sum(tsvd.explained_variance_ratio_)

def _trim_bounds(arr, bounds):
    

def plot_points(dim_red_func, docs):
    points, freq_ = dim_red_func(docs)
    print('total variance preserved: ' + str(freq_))

    fig = plt.figure()
    ax = plt.axes(projection ='3d')
    
    ax.set_xlim((-500,1200))
    ax.set_ylim((-3000,10000))
    ax.set_zlim((-8000,2000))
    
    ax.scatter3D(points.T[0], points.T[1], points.T[2], cmap ='black') 
    plt.show()

plot_points(get_tsvd, iterate_docs.get_docs())