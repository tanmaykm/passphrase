import string, random, hashlib

sysrand = random.SystemRandom()

class MarkovModel(object):
    def __init__(self, data, chain_length):
        self.data = data
        self.chain_length = chain_length
        self._model = None

    def __getstate__(self):
        if None == self._model:
            self.make_model()
        return [self.chain_length, self._model]
    
    def __setstate__(self, state):
        print("set state called with " + str(state))
        self.data = None
        self.chain_length = state[0]
        self._model = state[1]

    def model(self):
        return self._model if (self._model != None) else self.make_model()

    
    def make_model(self):
        model = {}
        data = self.data
        cl = self.chain_length
        for idx in range(0, len(data)-cl+1):
            key = tuple(data[idx:(idx+cl-1)])
            val = data[idx+cl-1]
            if not model.has_key(key):
                model[key] = { val: 1 }
            else:
                kd = model[key]
                if kd.has_key(val):
                    kd[val] += 1
                else:
                    kd[val] = 1
        
        for key in model.keys():
            kd = model[key]
            skv = sorted(zip(kd.values(), kd.keys()))
            vals = [v for (v,k) in skv]
            keys = [k for (v,k) in skv]

            tot = sum(vals)
            vals = [float(v)/tot for v in vals]
            model[key] = (tuple(keys), tuple(vals))
            
            
        self._model = model
        return model

    def start(self, rand_val=None):
        k = self.model().keys()
        if None == rand_val:
            rand_val = float(sysrand.randrange(1000))/1000
        return k[int((len(k)-1)*rand_val)]

    def next(self, curr, rand_val=None):
        #key_begin = curr[-self.chain_length:]
        m = self.model()
        keys,values = m[curr]
        if None == rand_val:
            rand_val = float(sysrand.randrange(1000))/1000
        cum_val = 0
        key = None
        for idx in range(0,len(keys)):
            key = keys[idx]
            val = values[idx]
            cum_val += val
            if cum_val >= rand_val:
                break
        return key

    def gen(self, len):
        lst = self.start()
        for idx in range(0, len):
            curr = lst[-(self.chain_length-1):]
            n = self.next(curr)
            lst = lst + (n,)
        return lst[self.chain_length-1:]


class CharMarkovModel(MarkovModel):
    """Chains characters in the document, disregarding anything other than aplhabets."""
    def __init__(self, text, chain_length):
        text = "".join([c if c in string.ascii_lowercase else '' for c in text.lower()])
        super(CharMarkovModel, self).__init__(text, chain_length)


class WordMarkovModel(MarkovModel):
    """Chains words in the document."""
    def __init__(self, text, chain_length):
        text = text.lower().split()
        super(WordMarkovModel, self).__init__(text, chain_length)

class WordBeginMarkovModel(CharMarkovModel):
    """Similar to CharMarkovModel, but ensures that the beginning is from a valid word."""
    def __init__(self, text, chain_length):
        wb = set()
        w = text.lower().split()
        begin_len = chain_length-1
        for idx in range(0,len(w)):
            word = []
            for c in w[idx]:
                if c in string.ascii_lowercase:
                    word.append(c)
            word = tuple(word[0:begin_len])
            if len(word) == begin_len:
                wb.add(word)
        self.word_begins = list(wb)
        super(WordBeginMarkovModel, self).__init__(text, chain_length)

    def start(self, rand_val=None):
        k = self.word_begins
        if None == rand_val:
            rand_val = float(sysrand.randrange(1000))/1000
        return k[int((len(k)-1)*rand_val)]

    def gen(self, len):
        lst = self.start()
        for idx in range(0, len-self.chain_length+1):
            curr = lst[-(self.chain_length-1):]
            n = self.next(curr)
            lst = lst + (n,)
        return lst


class SeededMarkovModel(object):
    def __init__(self, model, seed, true_random=False):
        self.model = model
        dig = [ord(x) for x in hashlib.sha1(seed).hexdigest()]
        s = sum(dig)
        self.dig = [float(x)/s for x in dig]
        if not true_random:
            self.dig = [self._seed_random(x) for x in dig]
        self.didx = 0

    def _seed_random(self, seed):
        random.seed(seed)
        return float(random.randrange(1000))/1000

    def start(self):
        self.didx = 0
        return self.model.start(self.dig[0])
    
    def next(self, curr):
        self.didx += 1
        if self.didx >= len(self.dig):
            self.didx = 0
        return self.model.next(curr, self.dig[self.didx])
    
    def gen(self, ln):
        lst = self.start()
        cl = len(lst)
        for idx in range(0, ln-cl):
            curr = lst[-cl:]
            n = self.next(curr)
            lst = lst + (n,)
        return lst

