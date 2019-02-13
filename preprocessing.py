from html import unescape
import string
import re


class Cleantext(object):
    def __init__(self):
        self.stp_wrd = ['zon', 'itu', 'loh', 'kan', 'hal', 'apa', 'aku', 'qur', 'bos', 'udd', 'fpd', 'sex', 'tan',
                        'sby', 'gedrun',
                        'pdh', 'sih', 'lho', 'nye', 'yuk', 'pas', 'kok', 'duh', 'feb', 'oce', 'you', 'pns', 'ytr',
                        'lah', 'kjp',
                        'gus', 'uda', 'and', 'bwt', 'deh', 'oke', 'lha', 'bud', 'elu', 'btp', 'ala', 'adl', 'bio',
                        'hah', 'woy',
                        'kab', 'sah', 'rot', 'wow', 'the', 'bbm', 'doi', 'ftv', 'yes', 'yak', 'gub', 'bir', 'pki',
                        'blm', 'sam',
                        'cnn', 'elo', 'gue', 'dua', 'emg', 'uma', 'gym', 'ehh', 'ira', 'cwe', 'gtu', 'die', 'dpp',
                        'url', 'met',
                        'csr', 'pun', 'tuk', 'uhm', 'yoi', 'god', 'grp', 'plt', 'ber', 'yos', 'aya', 'air', 'jam',
                        'one', 'cek',
                        'kpi', 'adh', 'eks', 'gen', 'oki', 'pan', 'tat', 'kel', 'bib', 'bgn', 'tuh', 'luh', 'hnw',
                        'koq', 'oom', 'hadisurya', 'hastag',
                        'sel', 'sie', 'kwi', 'omg', 'lol', 'fir', 'aun', 'man', 'oon', 'ilc', 'nol', 'mus', 'via',
                        'iva', 'din', 'dewobroto', 'sejunnie', 'gusnaidi', 'rabono', 'utenan', 'hasrini',
                        'apr', 'tol', 'kua', 'sia', 'isi', 'teh', 'bom', 'mng', 'user', 'dan', 'pak', 'ada', 'kau',
                        'kamu', 'saya', 'yang', 'ini', 'swt', 'nya', 'lagi', 'mas', 'dari', 'omdo', 'emakemak', 'meletek']

        self.slang_tbh = {"gla": 'gila', 'sok': 'sombong', 'tak': 'tidak', 'loh': 'kamu', 'non': 'tidak', 'liwat': 'lewat', 'pro': 'pendukung', 'cma': "cuma", 'kaga': 'tidak', 'kite': 'kita', 'ame': 'sama',
                          'maren': 'kemarin', 'muhammadi': 'muhamadiyah', 'ust': 'ustad', 'asu': 'anjing', 'kek': 'seperti', 'msh': 'masih', 'morfotin': 'mengambil', 'sehatkan': 'sehat', 'kerukukan': 'kerukunan',
                          'spt': 'seperti', 'tdi': 'tadi', 'cpt': 'cepat', 'kafr': 'kafir', 'smg': 'semoga', 'mrs': 'merasa', 'pastimenang': 'pasti menang', 'maluin': 'malu', 'jokopret': 'jokowi kampret',
                          'blg': 'bilang', 'blm': 'belum', 'jga': 'juga', 'gtu': 'gitu', 'pcetar': 'dicambuk', 'bru': 'baru', 'met': 'selamat', 'sejahterakan': 'sejahtera', 'kerjaanmu': 'kerjaan',
                          'tlah': 'telah', 'mgk': 'mungkin', 'pant': 'pantat', 'sul': 'sulawesi', 'bhs': 'bahasa', 'tsb': 'tersebut', 'bsa': 'bisa', 'mlyani': 'melayani', 'malteng': 'maluku tengah',
                          'pemaparantentang': 'pemaparan tentang', 'matimu': 'mati', 'inshaa': 'insyha', 'menemanin': 'nemanin', 'kampanyeahokjahat': 'kampanye ahok jahat', 'bejad': 'bangsat', 'nomorkoruptor': 'nomor koruptor',
                          'ahlaknya': 'akhlaknya', 'ahokdjarot': 'ahok djarot', 'salamjari': 'salam jari', 'djarotlah': 'djarot', 'jabatn': 'jabatan', 'bekasisah': 'bekas', 'tapinya': 'tapi'}

        self.translator = str.maketrans('', '', string.punctuation)

    @staticmethod
    def escapping_html(data):
        htmlp = unescape(data)
        return re.sub(r"https\S+", "", htmlp)

    def removepunc(self, text):
        clean_text = re.sub(r'(@\w*)|(#\w*)|\.(?!$-)|(\\w*)|(\?)', ' ', text)
        clean_text = " ".join(clean_text.split())
        return clean_text.translate(self.translator)

    #   memisahkan kata yang digabung
    @staticmethod
    def splitatacher(text):
        #   return " ".join(re.findall('[A-Z][^A-Z]*', text))
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', text)
        data = " ".join([m.group(0) for m in matches])
        data = re.sub(r'([a-zA-Z])([\W])', r'\1 \2', data)
        return data.split()

    def split_num_str(self, tst):
        hasiil = []
        datas = self.splitatacher(tst)
        for text1 in datas:
            dc = []
            for i in text1:
                if i.isdigit() or None:
                    continue
                dc.append(i)
            hasiil.append("".join(dc))
        return " ".join(hasiil)

    @staticmethod
    def __casefolding(textcor):
        return textcor.lower()

    @staticmethod
    def __tokenzing(termlist):
        return termlist.split()

    def conv_slangword(self,cortext, dataslang, cekdt=False):
        tweet = cortext.split()
        if cekdt:
            dataslang = dataslang
        else:
            dataslang = self.slang_tbh
        has = []
        for text in tweet:
            if text.lower() in dataslang:
                has.append(dataslang[text.lower()])
                continue
            has.append(text)
        return " ".join(has)

    def stop_word(self, stext, stop=None):
        tw = stext.lower().split()
        his = []
        for txt in tw:
            if txt not in self.stp_wrd and len(txt) > 2:
                his.append(txt)
        return " ".join(his)

    def proses_cleaning(self, corpus, slg, stp):
        tclean = []
        for text in corpus:
            clean = self.escapping_html(text)
            clean = self.split_num_str(clean)
            clean = self.removepunc(clean)
            clean = self.conv_slangword(clean, slg)
            clean = self.stop_word(clean, stp)
            tclean.append(clean.lower())

        return tclean


if __name__ == "__main__":
    data = [
        "RT @spardaxyz: Fadli Zon Minta Mendagri SegeraMenonaktifkan Ahok Jadi Gubernur DKI https:\/\/t.co\/@KH5vIRwPdO",
        "Pagi Ini Polrestro Bekasi Gelar Pasukan &amp; Pilkada https:\/\/t.co\/ypRv5nNjSb",
        "Ahok Akan Integrasikan Transportasi Publik dengan Sistem Single Ticketing\u2026 https:\/\/t.co\/42PH7pqV0b #infoTribun"
    ]

    clean = Cleantext()
    for dat in data:
        datcl = clean.escapping_html(dat)
        print(datcl)
        datcl = clean.split_num_str(datcl)
        print(datcl)
        datcl = clean.removepunc(datcl)
        print(datcl)
        print("------------------------")
