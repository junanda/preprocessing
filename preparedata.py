from core.preprocessing import Cleantext
import numpy as np
from model.dataof import Dataof

def cleankan(data, slang, dataf=True):
    dof = Dataof.dataall()
    clt = Cleantext()
    textclean = []
    labl = []
    for a in dof:
        if a['label'] == 'Non_HS':
            labl.append(0.)
        else:
            labl.append(1.)

        cln = clt.escapping_html(a['tweet'])
        cln = clt.split_num_str(cln)
        cln = clt.removepunc(cln)
        cln = clt.conv_slangword(cln, slang)
        cln = clt.stop_word(cln, ['user', 'rt', 'rk', 'hu', 'dan', 'pak'])
        textclean.append(cln.lower())

    x_data = np.zeros((len(textclean[1220:]), 33, 50), dtype=np.float64)

    return textclean[1220:], labl[1220:], x_data