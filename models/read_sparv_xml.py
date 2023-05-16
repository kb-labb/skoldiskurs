from lxml import etree
import string
import re

xml_file = "export.xml"

def read_xml(xml_file):
    parser = etree.XMLParser(recover = True)
    tree = etree.parse(xml_file, parser = parser)
    root = tree.getroot()

    lemmas = []

    for token in root.iter("token"):
        lemma = token.get("lemma")
        if lemma:
            lemmas.append(lemma)
        else:
            lemmas.append(token.text)

    return lemmas

def create_corpus(tokens):
    sents = []
    my_list = []
    punct = string.punctuation
    for token in tokens:
        if token == "." or token == "!" or token == "?":
            if len(my_list) > 0:
                sents.append(my_list)
                my_list = []
            else:
                my_list = []
        elif type(token) == str:
            if token in punct:
                pass
            else:
                my_list.append(token.strip().lower())
        if type(token) != str:
            my_list.append(token.strip())
    print(f"Number of sentences in the corpus: {len(sents)}.")
    return sents

def save_corpus(corpus):
    with open("outfile.txt", "w") as f:
        # Loop over each inner list and join the tokens back into sentences
        for sublist in corpus:
            corpus = ' '.join(str(v) for v in sublist)
            corpus = re.sub("[0-9]+", " ", corpus)
            corpus = re.sub("[^A-Za-zåäöÖÅÄ\s]", " ", corpus)
            # Write the sentence to the text file, followed by a new line character
            #print(corpus)
            f.write(corpus + '\n')


tokens = read_xml(xml_file)
sentences = create_corpus(tokens)
save_corpus(sentences)
