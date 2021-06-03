
import tensorflow.keras as keras
import utils
import d2v_model

fvs = []
d2v = d2v_model.get_d2v_model()

with open(utils.get_path('docs1.data'), 'r', encoding='utf8', errors='ignore') as f:
  for doc in f.readlines():
    fvs.append(d2v.infer_vector(doc.split(' ')))

print(fvs[0].shape)

model = keras.models.Sequential()
model.add(keras.Input(100))
model.add(keras.layers.Dense(40, activation='relu'))
model.add(keras.layers.Dense(1, activation='relu'))

model.save('my_model')
