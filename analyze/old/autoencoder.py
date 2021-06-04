
from tensorflow import keras
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

orig_dim = 3

def gen_3d_circle_data(t):
  return np.outer(np.cos(t), np.asarray([1,1,1])) + np.outer(np.sin(t), np.asarray([1,-2,1]))

def rand_angle(num_samples):
  return 2*np.pi*np.random.rand(num_samples)

def get_data(noise_frac, num_samples):
  return gen_3d_circle_data(rand_angle(num_samples))+noise_frac*np.random.multivariate_normal(np.zeros(orig_dim), np.eye(orig_dim), num_samples)

def get_models():

  enc_dim = 2

  inp_layer = keras.Input(shape=orig_dim)
  encode_layer = keras.layers.Dense(enc_dim, activation="relu")(inp_layer)
  decode_layer = keras.layers.Dense(orig_dim, activation="sigmoid")(encode_layer)

  encoded_input = keras.Input(shape=enc_dim)

  encoder = keras.Model(inp_layer, encode_layer)
  model = keras.Model(inp_layer, decode_layer)
  decoder = keras.Model(encoded_input, model.layers[-1](encoded_input))

  return encoder, decoder, model

encoder, decoder, autoencoder = get_models()

autoencoder.compile(loss="mean_squared_error", optimizer="adam")
X = get_data(0, 10000)

print(encoder.weights)

autoencoder.fit(X, X)

points = decoder.predict(encoder.predict(X))

print(encoder.weights)

plt.scatter(X.T[0], X.T[1], c='blue')
plt.scatter(points.T[0], points.T[1], c='red')
plt.show()