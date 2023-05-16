# skoldiskurs
Forskningsprojekt Handelshögskolan.

Here, we outline the pipeline of Ema's project, from data collection and parsing to training and using the vector representations.

Pipeline is largely as follows:

1. Download data from riksdagens open data.
2. Run sparv pipeline to tokenize and extract lemmas.
3. Parse data and transform to datafiles (using create_datafile.py and clean_corpus.py)
4. Train vectors with train_sentence.py.
5. Use vectors.

The corpora we are working with is two-fold: a political corpus and a newspaper corpus. The political corpus consists of the following data sources:

1. Riksdagens anföranden.

   1.1. To download riksdagens anföranden, we have to use to scripts: data_scripts/anforanden/download_anforanden_1962-1992.sh and data_scripts/anforanden/download_anforanden_1993-2023.sh. These scripts require no input (apart from changing some hardcoded paths) and can be run as is. Execution of the scripts generate (1) a directory anforanden_1993-2023_json where source files from 1993-2023 are stored and (2) a git clone of the state riksdagen-corpus which is a curated and partially manually corrected of older anföranden, within the welfare-state-analytics project run by Måns Magnusson. The files from 1993 and forward is generally of high quality while the older anföranden have some data quality issues, partically mitigated in the riksdagen-corpus.


   1.2. To parse riksdagens anföranden, there is two scripts (due to the different sources of the data): parse_anforanden_1962-1992.py and parse_anforanden_1962-1992.py and parse_anforanden_1993-2023.py. The scripts require no user input (apart from changing some hardcoded paths) and should generate two parquet dataframes: anforanden_1993-2023.parquet and anforanden_1962-1992.parquet.

2. Riksdagens motioner.

   2.1. The pipeline for riksdagens motioner is largely the same as for anforanden. The scripts data_scripts/motioner/download_motioner_2014-2023.sh and data_scripts/motioner/download_motioner_2014-2023.sh generated two dirs of json files: motioner_1971_2013_json and motioner_2014-2023_json. Data from 1962-1970 is missing from riksdagens datasets and is therefore not included. There are some pdf:s available for download on riksdagens hemsida. That is on my to do list.

   2.2. To parse motioner, use data_scripts/motioner/parse_motioner_1971-2013.py and data_scripts/parse_motioner_2014-2023.py. These scripts generate two dataframes stored in parquet files, which is the data we will be using to create our cectors. All older files (both motioner and anföranden) result in less detailed dataframes, consisting of document id:s (of varying quality), text and dates.


The data is tokenized and lemmatized using the sparv pipeline. The pipeline results in a number of xml files that are consequently parsed and transformed to a txt file with one sentence per line.