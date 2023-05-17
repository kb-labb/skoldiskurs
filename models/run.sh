#!/bin/bash

# TO DO Fix var names
OUTPUTDIR=$1 # Is output dir where all files are located.
CONCATENATEDFILE=$2 # Concatenated file name
BINFIL=$3

echo "starting vectorization..."
cd $OUTPUTDIR; cat *_export.txt > $CONCATENATEDFILE.txt; rm *_export.txt; cd /home/hilhag/prjs/skoldiskurs/models/
#python3 train_sentence.py --o $3 --c $1$2.txt --v 300 --a 0.05 #&& \
#python3 train_sentence.py --o "300v_2021_dn_token_lr0.1.bin" --c "export.xml" --v 300 --a 0.1
