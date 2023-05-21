import stanza
import pandas as pd
import os
import re

corpus_dir = "/home/hilhag/prjs/sprakbanken/corpus/"
years = list(range(1980, 1981))

for year in years:
    out_file = open("/home/hilhag/prjs/sprakbanken/corpus/1982/source/stanza_tokens.txt", "a")  # append mode
    # create write file here in append mode
    files = os.listdir(corpus_dir + str(year) + "/source/")
    for file in files:
        file_name = corpus_dir + str(year) + "/source/" + file

        nlp = stanza.Pipeline("sv", processors="tokenize, lemma", tokenize_batch_size=4)
        with open(file_name, "r") as f:
            doc = nlp(f.read())

            for sentence in doc.sentences:
                sent = []
                for word in sentence.words:
                    sent.append(word.lemma)
                #sent_string = " ".join(sent)
                sent_string = ' '.join(str(v) for v in sent) # Justyna's cleaning here for commensurability
                sent_string = re.sub("[0-9]+", " ", sent_string)
                sent_string = re.sub("[^A-Za-zåäöÖÅÄ\s]", " ", sent_string)
                print(sent_string)
                out_file.write(sent_string.lower() + "\n")
