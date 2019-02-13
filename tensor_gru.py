import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from scipy.spatial.distance import cdist
from tensorflow.python.keras.models import Sequential, model_from_json
from tensorflow.python.keras.layers import Dense, GRU, Flatten
from tensorflow.python.keras.optimizers import Adam, SGD


class GRUTheano:
    def __init__(self, input_x, hidden_layer, epoch=20, lr=1e-3, optimasi='SGD'):
        self.input = input_x
        self.hidden_layer = hidden_layer
        self.epoch = epoch
        self.lr = lr
        self.feat_max = 50
        self.optim = optimasi
        self.__build_model__()

    def __build_model__(self):
        self.model = Sequential()
        self.model.add(GRU(units=self.hidden_layer, return_sequences=True, input_shape=(self.input, self.feat_max)))
        self.model.add(Flatten())
        self.model.add(Dense(1, activation='sigmoid'))
        if self.optim == 'Adam':
            optimasi = Adam(lr=self.lr)
        else:
            optimasi = SGD(lr=self.lr)
        self.model.compile(loss='binary_crossentropy', optimizer=optimasi, metrics=['accuracy'])

    def feedpassward(self, data_train, label_train, batc=100):
        history = self.model.fit(data_train, label_train, validation_split=0.05, epochs=self.epoch, batch_size=batc)
        return history

    def evaluasimodel(self, data_test, label_test):
        result = self.model.evaluate(data_test, label_test)
        #   print(result)
        print("Accuracy: {0:.2%}".format(result[1]))
        if result[1] > 0.90:
            self.simpan_model()

    def prediksi(self, data_prediksi, label_prediksi):
        y_predik = self.model.predict(x=data_prediksi)
        y_predik = y_predik.T[0]

        cls_pred = np.array([1. if p > 0.5 else 0. for p in y_predik])
        cls_true = np.array(label_prediksi)

        incorect = np.where(cls_pred != cls_true)
        print(incorect)
        incorect = incorect[0]
        print("incorect : ", incorect)
        print(len(incorect))

    def simpan_model(self):
        #   serialize model to json
        model_json = self.model.to_json()
        with open('berat/model.json', "w") as json_file:
            json_file.write(model_json)
        # serialize bobot to HDFS
        self.model.save_weights("berat/model.h5")
        print("model disimpan di disk")

def load_parameter(x, y, path='berat/model_10_sgd_beda.json', modelClass=GRUTheano):
    json_file = open(path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('berat/model_10_sgd_beda.h5')
    #print("loaded.... model from disk")

    loaded_model.compile(loss="binary_crossentropy", optimizer="SGD", metrics=["accuracy"])
    score = loaded_model.evaluate(x, y)
    #print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))
    #return loaded_model

if __name__ == "__main__":
    modl = GRUTheano(50, 100, epoch=100)