import pandas as pd
import os
import glob
import string 
import argparse
from tqdm import tqdm

# Creates an input file with one sentence per line for training of fasText models from a .csv with Sparv annotations. Texts are lowercased and interpunction is removed.

# TO DO
# Modify script to take xml as input

parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i", "--input")
parser.add_argument("-t", "--type", default="token", help="token, saldo, lemma") 
parser.add_argument("-o", "--output")
args = vars(parser.parse_args())


df = pd.read_csv(args["input"], index_col=None, header=0, engine="python")

def create_corpus():
    sents = []
    my_list = []
    punct = string.punctuation 
    for i in range(len(df)):
        if df.loc[i, 'token'] == "." or df.loc[i, 'token'] == "!" or df.loc[i, 'token'] == "?":
            if len(my_list) > 0:
                sents.append(my_list)
                my_list = []
            else:
                my_list = []
        elif type(df.loc[i, args["type"]]) == str:
            if df.loc[i, 'token'] in punct:
                pass
            else:
                my_list.append(df.loc[i, args["type"]].lower())
        if args["type"] == "token":
            if type(df.loc[i, 'token']) != str:
                my_list.append(df.loc[i, 'token'])
        elif args["type"] == "SALDO sense" or args["type"] == "lemma":
            if pd.isna(df.loc[i, args["type"]]) or df.loc[i, args["type"]] is None:
                if str(df.loc[i, 'token']) in punct:
                    pass
                else:
                    try:
                        my_list.append(df.loc[i, 'token'].lower())
                    except:
                        my_list.append(df.loc[i, 'token'])
    print(f"Number of sentences in the corpus: {len(sents)}.")
    return sents

def save_corpus(corpus):
    with open(args["output"], 'w') as f:
        # Loop over each inner list and join the tokens back into sentences
        for sublist in corpus:
            corpus = ' '.join(str(v) for v in sublist)
            # Write the sentence to the text file, followed by a new line character
            f.write(corpus + '\n')

def main():
    print(args)
    corp = create_corpus()
    save_corpus(corp)

if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(time.time() - start)
