import stanza
import pandas as pd

#for col in anf_new.columns:
#    print(col)
#print(anf_new).head()

motioner_new = "/home/hilhag/prjs/skoldiskurs/data/motioner_2014_2023.parquet"
mot_new = pd.read_parquet(motioner_new)
mot_new = mot_new[mot_new['text'].notna()]
mot_new_df = mot_new['text'] # date var is "('year',)" # date is datum

anforanden_new = "/home/hilhag/prjs/skoldiskurs/data/anforanden_1993-2023.parquet"
anf_new = pd.read_parquet(anforanden_new)
anf_new = anf_new[anf_new['anforandetext'].notna()]
anf_new_df = anf_new["anforandetext"] # date variable is dok_datum

# Some super weird column formatting has accidentally happened in the older files
# The column names are as follows: ('dok_id',), ('text',), ('year',)
# TODO()
# Go back to parsing script and fix it
# List column command: print(anf_old.columns.tolist())
anforanden_old = "/home/hilhag/prjs/skoldiskurs/data/anforanden_1962-1992.parquet"
anf_old = pd.read_parquet(anforanden_old)
anf_old = anf_old[anf_old['(\'text\',)'].notna()]
anf_old = anf_old['(\'text\',)'] # date var is "('year',)"

motioner_old = "/home/hilhag/prjs/skoldiskurs/data/motioner_1971_2013.parquet"
mot_old = pd.read_parquet(motioner_old)
mot_old = mot_old[mot_old['(\'text\',)'].notna()]
mot_old_df = mot_old['(\'text\',)'] # date var is "('datum',)"

#df = pd.concat([mot_df, anf_df], axis=0)
#df = df.dropna()
#corpus = df.to_list()

#documents = corpus[0:10]

#out_docs = []
#nlp = stanza.Pipeline("sv", processors="tokenize, lemma", tokenize_batch_size=4)

#out_file = open("test.txt", "a")  # append mode

#i = 1
#for d in corpus:
#    print("Processing document ", str(i))
#    out_doc = nlp(d)
#    for sentence in out_doc.sentences:
#        sent = []
#        for word in sentence.words:
#            sent.append(word.lemma)
#        sent_string = " ".join(sent)
#        out_file.write(sent_string.lower() + "\n")
#        #print(sent_string.lower())
#    print("Document finished.")
#    documents_left = len(corpus) - i
#    print("Documents left to go:", str(documents_left))
#    i += 1

#####in_docs = [stanza.Document([], text=d) for d in documents] # Wrap each document with a stanza.Document object
#####out_docs = nlp(in_docs) # Call the neural pipeline on this list of documents
#####print(out_docs)



