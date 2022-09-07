#reference: https://stackoverflow.com/questions/29805642/learning-to-parse-a-fasta-file-with-python
import pandas as pd
import numpy as np
from read_fasta import *
from write_fasta import *
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', required=True, type = str, help = 'Name of human reference genome fasta file.') 
parser.add_argument('-r', '--result_dir', required = True, type = str, help = 'Directory where the resulting files will be made.')
args = parser.parse_args() 


chr_to_seq = read_fasta(args.filename)

chrs=list(chr_to_seq.keys())
seqs=list(chr_to_seq.values())

# Exclude selected chromosomes
exclude_chr = ['chr22','chrX','chrY']
include_chr_index = []
for i in range(len(chrs)):
    if chrs[i] not in exclude_chr:
        include_chr_index.append(i)
        
chrs_sampled=[]
seqs_sampled=[]
for i in range(len(include_chr_index)):
    chrs_sampled.append(chrs[include_chr_index[i]])
    seqs_sampled.append(seqs[include_chr_index[i]])
    

# If output directory doesn't exist, make one before writing result file
if not os.path.exists(args.result_dir):
    os.makedirs(args.result_dir)
    

# Write result as fasta file 
fname = os.path.join(args.result_dir, 'hg38_wo_22XY.fa') 
write_fasta_list(fname, chrs_sampled, seqs_sampled)
