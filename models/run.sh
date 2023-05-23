#!/bin/bash

OUTPUTDIR=$1 # Is output dir where all tokenized and lemmatized files are located.
CONCATENATEDFILE=$2 # The name of the concatenated file
BINFIL=$3 # Name of model


#cd $OUTPUTDIR; cat *_export.txt > $CONCATENATEDFILE.txt; rm *_export.txt; cd /home/hilhag/prjs/skoldiskurs/models/
echo "init vectorization..."
python3 train_sentence.py --o /home/hilhag/prjs/skoldiskurs/vectors/$3 --c $1$2
echo "Finished vector model."
#python3 train_sentence.py --o "300v_2021_dn_token_lr0.1.bin" --c "export.xml" --v 300 --a 0.1
