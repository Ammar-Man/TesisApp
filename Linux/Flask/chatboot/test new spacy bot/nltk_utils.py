# nltk_utils.py
import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

# Downloading if necessary
nltk.download('punkt')

stemmer = PorterStemmer()

# Tokenize a sentence
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Stem and lower each word
def stem(word):
    return stemmer.stem(word.lower())

# Create bag of words array
def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag
