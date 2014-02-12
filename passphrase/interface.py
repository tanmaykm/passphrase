import random, string, cPickle
from markov import WordBeginMarkovModel, SeededMarkovModel 


class Passphrase(object):
    UPPERCASE = 1
    LOWERCASE = 2
    MIXEDCASE = 3
    
    NUMERIC_REPL = ('begisozqjltdacfhkmnpruvwxy', 
                    '63915029117816606329402389')
    
    SPL_REPL = ('asivcykgqpbdhjlmnortuwxzef',
                '@$!^(/<&}{%#^!!&#@{|^=#.,*')
    
    UPPER_REPL = (string.ascii_lowercase, string.ascii_uppercase)
    
    def __init__(self, login_id="", website="", text_id="", passphrase="", length=16, ease=6, case=3, numeric=True, splchar=True):
        self.login_id = login_id
        self.website = website
        self.text_id = text_id
        self.passphrase = passphrase
        self.length = length
        self.ease = ease
        self.case = case
        self.numeric = numeric
        self.splchar = splchar
        self._model = None

    def _mk_model(self):
        if None != self._model:
            return
        
        try:
            self._model = self._load_model()
        except:
            text = open(self.text_id, 'r').read()
            phrase = ' '.join([self.login_id, self.website, self.passphrase])
            tm = WordBeginMarkovModel(text, self.ease)
            self._model = SeededMarkovModel(tm, phrase, False)
            #self._store_model()

    def _store_model(self):
        if None == self._model:
            return
        with open(self.text_id + '.model', 'wb') as f:
            cPickle.dump(self._model, f, -1)

    def _load_model(self):
        with open(self.text_id + '.model', 'rb') as f:
            return cPickle.load(f, -1)

    def password(self):
        self._mk_model()        
        s = ''.join(self._model.gen(self.length))
        
        #print("from model gen: " + s)
        if self.numeric:
            s = self._add_numeric(s)
            #print("after numeric replacement: " + s)
                
        if self.splchar:
            s = self._add_spl(s)
            #print("after special char replacement: " + s)
            
        if self.case == Passphrase.UPPERCASE:
            s = s.upper()
            #print("after up case: " + s)
        elif self.case == Passphrase.MIXEDCASE:
            s = self._add_upper(s)
            #print("after mix case: " + s)

        return s

    @staticmethod
    def find(s, ch):
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def _add_spl(self, s):
        nk = Passphrase.SPL_REPL[0]
        nv = Passphrase.SPL_REPL[1]
        return self._add_extra(s, nk, nv)

    def _add_numeric(self, s):
        nk = Passphrase.NUMERIC_REPL[0]
        nv = Passphrase.NUMERIC_REPL[1]
        return self._add_extra(s, nk, nv)

    def _add_upper(self, s):
        nk = Passphrase.UPPER_REPL[0]
        nv = Passphrase.UPPER_REPL[1]
        return self._add_extra(s, nk, nv)
        

    def _add_extra(self, s, nk, nv):
        s = list(s)
        nn = len(s)/8
        if (nn == 0):
            nn = 1
        
        kidx = 0
        while nn > 0:
            idxs = Passphrase.find(s, nk[kidx])
            if len(idxs) > 0:
                random.shuffle(idxs)
                s[idxs[0]] = nv[kidx]
                nn -= 1
            kidx += 1
            if kidx >= len(nk):
                kidx = 0
        return ''.join(s)

def password(login_id="", website="", text_id="", passphrase="", length=16, ease=6, case=3, numeric=True, splchar=True):
    return Passphrase(login_id, website, text_id, passphrase, length, ease, case, numeric, splchar).password()
