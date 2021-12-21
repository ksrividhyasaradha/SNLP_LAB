# -*- coding: utf-8 -*-
"""NLP_exp1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QqPSe4C6AM5R_edBLmM-i5xtoHGWHSjF
"""

#tokenization
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
text="""Here’s to the crazy ones, the misfits, the rebels, the troublemakers, the round pegs in the square holes. The ones who see things differently — they’re not fond of rules. You can quote them, disagree with them, glorify or vilify them, but the only thing you can’t do is ignore them because they change things. They push the human race forward, and while some may see them as the crazy ones, we see genius, because the ones who are crazy enough to think
that they can change the world, are the ones who do."""

word_tokenize(text)

#tokenization using gensim
from gensim.utils import tokenize
words=list(tokenize(text))
words

#tokenization with tweet data:
tweetdata="""https://t.co/9z2J3P33Uc FB needs to hurry up and add a laugh/cry button. Since eating my feelings has not fixed the world's problems, I guess I'll try to sleep... HOLY CRAP: DeVos questionnaire appears to include passages from uncited sources https://t.co/FNRoOlfw9s well played, Senator Murray Keep the pressure on: https://t.co/4hfOsmdk0l @datageneral thx Mr Taussig It's interesting how many people contact me about applying for a PhD and don't spell my name right."""
tweetdata

from nltk.tokenize import word_tokenize
word_tokenize(tweetdata)

compare_list = ['https://t.co/9z2J3P33Uc',
               'laugh/cry',
               "world's problems",
               "@datageneral",
                "It's interesting",
               "don't spell my name right",
               'all-nighter']
word_tokens = []
for sent in compare_list:
    print(word_tokenize(sent))
    word_tokens.append(word_tokenize(sent))

words

#ngrams
import pandas as pd
n=int(input())
n_grams=pd.Series(nltk.ngrams(words, n))
n_grams

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
example_sent="""Here’s to the crazy ones, the misfits, the rebels, the troublemakers, the round pegs in the square holes. The ones who see things differently — they’re not fond of rules. You can quote them, disagree with them, glorify or vilify them, but the only thing you can’t do is ignore them because they change things. They push the human race forward, and while some may see them as the crazy ones, we see genius, because the ones who are crazy enough to think
that they can change the world, are the ones who do."""
word_tokens = word_tokenize(example_sent)
 
filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
 
filtered_sentence = []
 
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)
 
print(word_tokens)
print(filtered_sentence)

#remove HTML tag
import re
text="<p>This is the first NLP exp</p>"
import re
clean = re.compile('<.*?>')
text= re.sub(clean, '', text)
text

#remove URLs
import re
text="https://t.co/9z2J3P33Uc FB needs to hurry up and add a laugh/cry button"
import re

text= re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

text

#tf -idf
import math
doc1 = ["Java is to JavaScript what car is to Carpet", 
        "I learned the fundamentals for programming, which is just what I needed as a first step for my career change", 
        "Learning to code is useful no matter what your career ambitions are"]
doc2 = ["First, solve the problem. Then, write the code", 
        "I came in with near zero programming knowledge and halfway in, I am quite confident of what I can achieve",
        "When you throw yourself out there great things happen"]
doc1_tokens = sum([doc.lower().replace(',', '').replace('.', '').split() for doc in doc1], [])
doc2_tokens = sum([doc.lower().replace(',', '').replace('.', '').split() for doc in doc2], [])
stopwords = ['a', 'the', 'i', 'me', 'myself', 'our', 'ourself', 'you', 'is', 'to', 'then', 'what', 'their', 'are', 'your', 
             'for', 'my', 'as', 'which', 'just', 'can', 'and', 'in', 'of', 'am', 'when', 'there', 'at', 'it', 'if']

doc1_tokens = set(doc1_tokens) - set(stopwords)
doc2_tokens = set(doc2_tokens) - set(stopwords)
unique_tokens = set(doc1_tokens).union(set(doc2_tokens))
count_doc1 = dict.fromkeys(unique_tokens, 0)
for token in doc1_tokens:
    count_doc1[token] += 1
count_doc2 = dict.fromkeys(unique_tokens, 0)

for token in doc2_tokens:
    count_doc2[token] += 1
def calculate_tf(count_doc, doc_tokens):
    tf = dict()
    for token, count in count_doc.items():
        tf[token] = count / float(len(doc_tokens))
    return tf
    
tf1 = calculate_tf(count_doc=count_doc1, doc_tokens=doc1_tokens)
tf2 = calculate_tf(count_doc=count_doc2, doc_tokens=doc2_tokens)
def calculate_idf(doc_counts):
    idf = dict.fromkeys(doc_counts[0].keys(), 0)
    for doc in doc_counts: 
        for token, count in doc.items():
            if count!=0:
                idf[token] += 1
                
    for token, count in idf.items():
        idf[token] = math.log(len(doc_counts) / float(count))
       
    return idf

idf = calculate_idf([count_doc1, count_doc2])
print(idf)


def calculate_tfidf(tf, idf):
    tfidf = dict()
    for token, count in tf.items():
        tfidf[token] = count * idf[token]
    return tfidf
tfidf1 = calculate_tfidf(tf1, idf)
tfidf2 = calculate_tfidf(tf2, idf)
tfidf_df = pd.DataFrame([tfidf1, tfidf2])
tfidf_df