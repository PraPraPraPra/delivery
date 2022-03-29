import os
import re
# import from nltk the functions that split a text into sentences and tokens
from nltk.tokenize import sent_tokenize, word_tokenize
from pprint import pprint
import zipfile

import pandas as pd
import numpy as np
from nltk import word_tokenize, pos_tag, chunk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
import logging

from ggeop_skill_transform_v4 import skill_transform;


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# The first time using nltk, you should run:
# import nltk
# nltk.download()
# ---- OR ----
# import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('stopwords')



"""
Problems:

Erros na lematização:
    ex.: EE e Java EE não são a mesma coisa (Electrical Engeneering e Java Enterprise Edition);
    ex.: muitas palavras com "/" -> A barra tem que ser " "(espaço)


"""
#Load the entire dataset
data = pd.read_csv('data/ggeop/JobsDataset.csv', header = 0, names = ['Query', 'Job Title', 'Description'])


(cleaned_description, max_size, version) = skill_transform(data)

#Create model
#model = Word2Vec(cleaned_description , size=100, window=5, min_count=1, workers=4)
# There was this error: TypeError: __init__() got an unexpected keyword argument 'size'
# Assumo size is now vector_size....

#Mudeio window_size para englobar a oferta toda - Funciona muito melhor!!!
model = Word2Vec(cleaned_description , vector_size=100, window=max_size, min_count=5, workers=6)
#model = Word2Vec(cleaned_description , vector_size=100, window=100, min_count=5, workers=4) #teste com window=100

#model = Word2Vec(cleaned_description , vector_size=100, window=5, min_count=5, workers=4)


#Para o outro modelo era:
#model = gensim.models.Word2Vec(my_list,  min_count=5, workers=4, epochs=25, sg=1, window=960)


#Skills Similarity
with open(f'data/ggeop/answer_{version}.txt', 'w') as f:            

    for seed_word in [ 'python', 'java', 'data', 'c', 'html', 'javascript', 'angular']:
        answer = model.wv.most_similar(positive=[seed_word], topn=10)

        print(seed_word, answer)
        print("\n")
        f.write(f'{seed_word} : {answer}\n')
