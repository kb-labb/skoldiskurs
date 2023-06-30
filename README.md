## A longitudinal study of political school discourse 1962-2023

This codebase contains all produced material for Ema Demir’s (ongoing) research project on Swedish school discourse in a political setting from 1962 to 2023. Here, we have created the tools to study the semantic shift on lexical units related to schools.

We do this by producing multiple vector representation of political text data using fastText embeddings, which is an extension of the word2vec model. We divide the data into buckets representing a time period. The periods at hands are chosen using two different approaches:

A theory driven approach of five buckets that are motivated by real world events (political decisions, school reforms etc). These events are better explained by Ema Demir herself. The periods are as follows:
- 1962-1967
- 1968-1980
- 1981-1991
- 1992-2011
- 2012-2023

Regular intervals à 5 years:
- 1962-1967
- 1968-1973
- 1974-1979
- 1980-1985
- 1986-1991
- 1992-1997
- 1998-2003
- 2004-2009
- 2010-2015
- 2016-2023

The political time buckets are also paired with what we might call control data, i.e newspaper texts from the corresponding time periods. These serve as kind of a control group in our experiments. KBLab has an ongoing collaboration with Språkbanken Text where we are training newspaper text representations for Språkbanken to be used in research. Therefore, we have been able to use these embeddings as well. They were trained by Justyna Sikora at KBLab with data sampled from the four biggest newspapers during the 1962-2021 (data from 2022 and 2023 were not available for this dataset). Note that data is sampled from the newspapers, making the underlying corpus slightly smaller than the political corpus. This can be adjusted at a later time if it turns out to be a problem. Under directory documentation, you’ll find a CSV with vector representation sizes in megabytes (MB).

The core idea of the research methodology is to be able to compare the semantic shift of words and phrases using models with text representation based on data from different periods of time. We do this by creating ```fastText``` vector representations of the texts. There are other available models, but we chose fastText in part because of KBLab’s collaboration with Språkbanken but also because of the user-friendly interface. Text representations are created using fastText implementation in [gensim](https://radimrehurek.com/gensim/models/fasttext.html). It is a fast C implementation of fastText with a Python interface. Gensim offers a streamlined training option with fewer options and parameters to control the training process, which has both pros and cons. This reduces flexibility but simplifies usages, which in this specific application is an attractive feature. For example, it allows easy loading and offers compatibility with other gensim functionalities.

Gensim’s implementation of fastText also extends beyond the original Facebook implementation by providing some additional functionality. For example, it includes methods for miscellaneous similarity queries. Another motivation is the fact that the gensim implementation is widely used in the Python ecosystem.

A detailed description of the process can be found in documentation/process.md.

##fastText model

fastText is a vector embedding model for representing and understanding text. It captures semantic meaning of words while considering morphological variations. 

A key aspect of fastText are subword embeddings. Not only does fastText capture semantic meaning of lexical units like words, but it also considers subword information, making it effective for handling features such as prefixes, suffixes and out-of-vocabulary words. fastText does this by breaking words down into subword units called character n-grams. These character n-grams can be as short as a single character or as long as the whole word. By considering these subword units, fastText is able to learn representations for words that contain similar character sequences, even if they are morphologically different.

In the training process, a continuous bag-of-words (CBOW) model predicts the probability of a word based on context, just like Word2Vec. But instead of predicting whole words, fastText predicts the probability of each subword given the context. By considering subwords, fastText can generate word representations even for unseen or misspelled words by leveraging the embeddings of their constituent subwords. Compared to Word2Vec, fastText is efficient. The use of subword units reduces the vocabulary size and enables fastText to handle a large number of words, including rare or out-of-vocabulary words. This, in turn, creates robust representations. 

##Usage

This is not a comprehensive guide to using gensim fastText. It is specifically aimed at Ema. So, open terminal as previously instructed. Open the Python interactive shell, in which we will perform our analyses, by typing:

```
python3
```

In the resulting shell, type:

```
from gensim.models import FastText
```

To load a model, type:

```
model = FastText.load("model.bin")
```

The file name is ```model.bin``` so you need to replace this with the full name of the actual file, including the path, which is where the file is stored on your computer. I think it’s something like ```/Users/emademir/Documents/politics/``` and the file naming scheme is as follows: ```1981_1991_lemmatized.bin``` making the full path to the file ```/Users/emademir/Documents/politics/1981_1991_lemmatized.bin```. If this is the case, you can load the model like this:

```
model = FastText.load("/Users/emademir/Documents/politics/1981_1991_lemmatized.bin")
```

Also note that you can load multiple models and keep them in memory. To do this, modify the name of the model to a unique name, for example ```model_1```, ```model_2``` etc instead of ```model``` as in the example above.. Some similarity functions are listed below but I will also refer to some tutorials that might be helpful.

Get similarity of two terms:

```
model.wv.similarity("elev", "lärare")
```

Similarity of two sets of vectors:

```
model.wv.n_similarity(["elev", "lärare"], ["skola", "undervisning"])
```

Get most similar words:

```
model.wv.most_similar("elev")
```

Do some word arithmetics:

```
model.wv.most_similar(positive=["lärare", "rektor"], negative=["elev"])
```
Find words that do not match the context:

```
model.wv.doesnt_match("lärare elev undervisning pommac".split())
```

## Some methodological choices
Models that intrinsically track semantic and lexical change are still experimental.
Here, we need to do some justification as to why 

## Evaluation
No evaluation, other than ocular inspection, has been performed at this time. Some inspiration can be found here:
- https://web.stanford.edu/~jurafsky/slp3/6.pdf (section 6.10.1)
- https://cocosci.princeton.edu/papers/nematzadeh_etal_17_cogsci_reps.pdf
- https://aclanthology.org/W16-2513.pdf

## Resources
Good tutorial on similarity operations can be found here: https://notebook.community/ELind77/gensim/docs/notebooks/FastText_Tutorial

Here is a link to future me with some quantitative eval inspiration: 
https://github.com/PacktPublishing/fastText-Quick-Start-Guide/blob/master/chapter5/fasttext%20with%20gensim.ipynb

Further explanation of fastText model: https://towardsdatascience.com/word-embedding-with-word2vec-and-fasttext-a209c1d3e12c

Official documentation of gensim fastText: https://radimrehurek.com/gensim/models/fasttext.html
