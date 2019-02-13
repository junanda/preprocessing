from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from pymongo import MongoClient
from core.preprocessing import Cleantext
from core.word2vec import load_model
import numpy as np
from sklearn import metrics
from core.utils import calculasi
import random, pickle


class MeanEmbeddingVectorize(object):
    def __init__(self, word2vec):
        self.word2v = word2vec
        self.dim = 200

    def fit(self, x, y):
        return self

    def transform(self, x):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in x
        ])


def meanembedding(datapakai, feature, word2vector):
    datask = np.zeros((len(datapakai), len(feature)), dtype=np.float64)

    for index, tweet in enumerate(textclen):
        for tem in tweet.split():
            if tem in word2vector.wv.vocab:
                #datask[index, feature.index(tem)] = np.mean(word2vector.wv.get_vector(tem))
                datask[index, feature.index(tem)] = np.sum(word2vector.wv.get_vector(tem))

    return datask


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client.social
    cl = Cleantext()

    stp = db.storetext.find({'name': 'stopword'})
    data_stp = stp[0]["data"]
    slg = db.storetext.find({'name': 'slangword'})
    data_slang = slg[0]["data"]

    try:
        word_vector = load_model('../data/model/200/W2vec_wiki_id_5.bin')

        textclen = []
        label = []

        datapk = pickle.load(open('datasimpan.pkl', 'rb'))

        for a in datapk:
            if a['label'] == 'Non_HS':
                label.append(0.)
            else:
                label.append(1.)
            clean1 = cl.escapping_html(a['tweet'])
            clean1 = cl.split_num_str(clean1)
            clean1 = cl.removepunc(clean1)
            clean1 = cl.conv_slangword(clean1, data_slang)
            clean1 = cl.conv_slangword(clean1, data_slang, True)
            clean1 = cl.stop_word(clean1)
            textclen.append(clean1.lower())
        print(textclen)
        count_vec = CountVectorizer()
        dataall = count_vec.fit_transform(textclen)
        data_array = dataall.toarray()

        tfidf = TfidfVectorizer()
        datatfidf = tfidf.fit_transform(textclen)

        feat_term = count_vec.get_feature_names()

        data_pk = meanembedding(textclen, feat_term, word_vector)

        clf = RandomForestClassifier(n_estimators=20, criterion="entropy", max_depth=150).fit(data_pk[:1220], label[:1220])
        #clf1 = LinearSVC().fit(data_pk[:1220], label[:1220])
        #clf2 = LinearSVC().fit(datatfidf[:1220], label[:1220])
        #cls1 = BernoulliNB().fit(datatfidf[:1220], label[:1220])
        #blr = LogisticRegression().fit(datatfidf[:1220], label[:1220])
        #rfdt = RandomForestClassifier(n_estimators=20, criterion="entropy", max_depth=150).fit(datatfidf[:1220], label[:1220])


        predicts = clf.predict(data_pk[1220:])
        #predicts2 = clf1.predict(dataall[1220:])
        #predicts3 = clf2.predict(datatfidf[1220:])
        #predicts4 = rfdt.predict(datatfidf[1220:])

        #print(metrics.classification_report(label[1220:], predicts))
        #print(metrics.classification_report(label[1220:], predicts2))
        #print(metrics.classification_report(label[1220:], predicts3))
        #print(metrics.classification_report(label[1220:], predicts4))

        acc, prec, rec, f1 = calculasi(predicts, label[1220:])
        #acc2, prec2, rec2, f12 = calculasi(predicts2, label[1220:])
        #acc3, prec3, rec3, f13 = calculasi(predicts3, label[1220:])

        print("Hasil data w2v : ", prec, rec, f1, acc )
        #print("Hasil data tf : ", prec2, rec2, f12, acc2 )
        #print("Hasil data tf-idf : ", prec3, rec3, f13, acc3 )
        if acc >= 89.53:
            print(" menyimpan model ... ")
            with open("../berat/supervised_model/rfdt/rfdt_sum_m2v.pkl", "wb") as wrt:
                pickle.dump(clf, wrt)
            print(" model berhasil disimpan di disk...")

    except Exception as e:
        print(e)
