from __future__ import print_function
from gensim.corpora import WikiCorpus
import logging
import os.path
import sys

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s ')
    logging.root.setLevel(level=logging.INFO)
    logging.info("running %s" % ' '.join(sys.argv))

    nameFileIn = "../data/idwiki-latest-pages-articles.xml.bz2"
    nameFileOut = "wiki.id.Case.text"

    space = " "
    i = 0

    #output = open('../data/'+nameFileOut, 'w')
    wiki = WikiCorpus(nameFileIn, lemmatize=False, dictionary={}, lower=False)
    for text in wiki.get_texts():
        #output.write(' '.join(text) + '\n')
        i += 1
        if i % 10000 == 0:
            logger.info("saved " + str(i) + " articles")

    #output.close()
    logger.info("Finished Saved " + str(i) + " articles")
