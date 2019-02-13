from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import multiprocessing
import logging
import os.path
import sys


def buatmodel(filein, output):
    # params = {'size':100, 'window': 5, 'min_count': 5, 'workers': max(1, multiprocessing.cpu_count() - 1),
    # 'sample': 1E-3,}

    params = {'size': 200, 'window': 5, 'min_count': 2, 'workers': multiprocessing.cpu_count(), }
    md = Word2Vec(LineSentence(filein), **params)
    md.init_sims(replace=True)
    md.save(output)
    #   md.wv.save_word2vec_format(output)


def load_model(filemodel):
    return Word2Vec.load(filemodel)
    #   return word2vec.KeyedVectors.load_word2vec_format(filemodel, binary=True)


def weigth_word(kata, mod):
    wordd = []
    try:
        #   hasil = model.most_similar(w, topn=6)
        for term in kata:
            if term in mod.wv.vocab:
                wordd.append(mod.wv.get_vector(term))
            #   else:
                #   print("kata", term)
        #   print(wordd[0])
        return wordd
    except KeyError as e:
        print(e)


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s ')
    logging.root.setLevel(level=logging.INFO)
    logging.info("running %s" % ' '.join(sys.argv))

    fileinput = '../data/wiki.id.tambah.case.text'
    fileout = '../data/model/200/W2vec_wiki_id_5.bin'

    #   buatmodel(fileinput, fileout)

    model = load_model(fileout)
    #model2 = load_model('../data/model/200/W2vec_wiki_id_10.bin')

    kata = ['agar', 'pers', 'menteri']
    for k in kata:
        if k in model.wv.vocab:
            print(k ," : ", model.wv.get_vector(k))
            print("----------------")
    #data5 = model.wv.similar_by_word(kata, topn=10, restrict_vocab=None)
    #data10 = model2.wv.similar_by_word(kata, topn=10, restrict_vocab=None)
    #print(model.wv.similarity("penista", "agama"))
    #print(model2.wv.similarity("penista", "agama"))
    #print(len(model.wv.vocab.items()))