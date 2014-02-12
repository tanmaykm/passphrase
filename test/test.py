from passphrase import password, Passphrase
from passphrase.markov import CharMarkovModel, WordMarkovModel, WordBeginMarkovModel, SeededMarkovModel
import sys, random, string

TRAINING_FILE = "animal_farm.txt"

def test_char(text):
    print("generating markov letter chains:")
    tm = CharMarkovModel(text, 5)
    for idx in range(1,5):
        s = ''.join(tm.gen(16))
        assert len(s) == 16
        print("\t" + s)


def test_wb_char(text):
    print("generating markov letter chains beginning with valid word:")
    tm = WordBeginMarkovModel(text, 5)
    for idx in range(1,5):
        s = ''.join(tm.gen(16))
        assert len(s) == 16
        print("\t" + s)


def test_word(text):
    print("generating markov word chains: ")
    tm = WordMarkovModel(text, 2)
    for idx in range(1,5):
        s = ' '.join(tm.gen(20))
        print("\t..." + s + "...")
    
def test_char_with_passphrase(text, phrase):
    print("generating letter chains with phrase as seed:")
    tm = WordBeginMarkovModel(text, 5)
    for idx in range(1,5):
        seededtm = SeededMarkovModel(tm, phrase + str(idx), False)
        s = ''.join(seededtm.gen(16))
        assert len(s) == 16
        print("\t" + s)

#     for idx in range(1,5):
#         seededtm = SeededMarkovModel(tm, phrase + str(idx), True)
#         s = ''.join(seededtm.gen(16))
#         assert len(s) == 16
#         print("SeedMarkovModel (true random): " + s)


def test_raw(phrase):
    text = open(TRAINING_FILE, 'r').read()
    test_word(text)
    test_char(text)
    test_wb_char(text)
    test_char_with_passphrase(text, phrase)

def test_splchar_replacement(pp):
    choice = random.SystemRandom().choice
    s = ''.join(choice(string.ascii_lowercase) for x in range(16))
    print("\trandom string: " + s)
    s = pp._add_numeric(s)
    print("\tafter numeric replacement: " + s)
    s = pp._add_spl(s)
    print("\tafter special char replacement: " + s)
    s = pp._add_upper(s)
    print("\tafter upper casing: " + s)


def test_passphrase():
    print("\ntesting special character replacement:")    
    pp = Passphrase("myid@email.com", "email.com", TRAINING_FILE, "hello world1", 16, 3, 2, True, True)
    test_splchar_replacement(pp)
    
    print("\ntesting passphrase:")
    choice = random.SystemRandom().choice
    s = ''.join(choice(string.ascii_lowercase) for x in range(16))
    pp = password("myid@email.com", "email.com", TRAINING_FILE, s, 16, 3, 2, True, True)    
    print("got password: " + pp)


if __name__ == "__main__":
    test_raw(sys.argv[1])
    test_passphrase()
    