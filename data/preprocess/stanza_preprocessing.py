import stanza
import pandas as pd
import os
import re

# Do tokenization and lemmatization on sentence level with Stanza here. Input corpus in sparv format, outputs a txt file with all texts representing one year. It is important to us to get a good idea of the lexical item "skola" in a school context so we lemmatize all hjälpverb "skola" to other baseforms.

corpus_dir = "/home/hilhag/prjs/sprakbanken/corpus/"
years = list(range(1968, 2023))

for year in years:
    out_file = open(corpus_dir + str(year) + "/stanza_tokens_skall.txt", "a") # append mode
    files = os.listdir(corpus_dir + str(year) + "/source/")
    for file in files:
        try:
            file_name = corpus_dir + str(year) + "/source/" + file

            nlp = stanza.Pipeline("sv", processors="tokenize, lemma, pos", tokenize_batch_size=4)
            with open(file_name, "r") as f:
                doc = nlp(f.read())

                for sentence in doc.sentences:
                    sent = []
                    for word in sentence.words:
                        if word.text == "skall" or word.text == "ska":
                            sent.append("skall")
                            # TODO()
                            # baseform "skulle" will also be "skola" so let the baseform be "skulle"
                        else:
                            sent.append(word.lemma)
                    sent_string = ' '.join(str(v) for v in sent) # Justyna's cleaning here for commensurability
                    sent_string = re.sub("[0-9]+", " ", sent_string)
                    sent_string = re.sub("[^A-Za-zåäöÖÅÄ\s]", " ", sent_string)
                    out_file.write(sent_string.lower().strip() + "\n")
        except:
            print("Catch all except due to lack of file. This is probably a dir.")
