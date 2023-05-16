import stanza
import pandas as pd
import os

df = pd.read_parquet("political_corpus.parquet")

# CREATE CORPUS DIR adapted to sparv pipeline

corpus_dir = "/home/hilhag/prjs/skoldiskurs/corpus/"

for i in range(len(df)):
    date = str(df.iloc[i, df.columns.get_loc('datum')])
    year = date[0:4]
    if not os.path.exists(corpus_dir + year):
        os.mkdir(corpus_dir + year)
    if not os.path.exists(corpus_dir + year + "/source"):
        os.mkdir(corpus_dir + year + "/source")

    f = open(corpus_dir + year + "/source/" + str(i) + ".txt", "w")
    f.write(df.iloc[i, df.columns.get_loc('text')])
    f.close()
