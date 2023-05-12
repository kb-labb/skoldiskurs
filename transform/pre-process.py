import stanza
import pandas as pd

motioner_new = "/home/hilhag/prjs/skoldiskurs/data/motioner_2014_2021.parquet"
motioner_old = "/home/hilhag/prjs/skoldiskurs/data/anforanden_1993_2021.parquet"

mot_new = pd.read_parquet(motioner)
anf_new = pd.read_parquet(anforanden)

anf_df = anf["anforandetext"]
mot_df = mot["titel"] + ". " + mot["text"]

df = pd.concat([mot_df, anf_df], axis=0)
df = df.dropna()
corpus = df.to_list()

documents = corpus[0:10]

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



