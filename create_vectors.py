from gensim.models import FastText
import pandas as pd
from sentence_splitter import SentenceSplitter, split_text_into_sentences
import re


fil = "/home/jussik/Documents/vectors/issue/issue/dagens_nyheter_2021.jsonl.filtered.normalized.filtered.deduped.txt"
with open(fil, "r", encoding="utf8") as f:
    corpus = f.readlines() 


splitter = SentenceSplitter(language='sv') #input should be divided into tokenized sentences
corpus= [splitter.split(s) for s in corpus] #split into sentences 

corpus = [re.findall(r"[\w']+|[.,!?]", s.lower()) for sentence in corpus for s in sentence] #a very naive way to tokenize

print(len(corpus))

model = FastText(vector_size=100, window=5, min_count=5,  sg=1, negative = 10)  # instantiate model
model.build_vocab(corpus_iterable=corpus)
model.train(corpus_iterable=corpus, total_examples=len(corpus), epochs=5) 
model.save("model.bin") 