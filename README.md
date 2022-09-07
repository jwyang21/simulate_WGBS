# simulate_WGBS

## Overview 
Sampling sequencing reads, running sherman and running bismark.           
Final result file (.bam) used as simulated WGBS reads

## Installation
conda env create -f simulate_wgbs.yaml

## Input
hg38.fa
- a GRCh38 fasta file named 'hg38.fa' is needed.
- GRCh38 fasta file can be downloaded from NCBI.
  - GRCh38 download link (NCBI): https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/

## Run
command to run Snakefile: snakemake -j 10

## Visualize DAG of Snakefile workflow
snakemake -j --dag | dot -Tpng -o dag.png (Reference: https://haje01.github.io/2020/04/21/snakemake-tutorial.html)

## Result
files in 'meth_erosion' folder
- Final result file '/meth_erosion/All_Merged/merged_bismark_bt2.bam' is to be used as simulated WGBS reads.
- Using the sorted version of the above file, '/meth_erosion/All_Merged/merged_bismark_bt2_sorted.bam' is also possible.

## DAG visualization of Snakefile workflow: (also available from 'dag.png' uploaded in this github directory)
![dag](https://user-images.githubusercontent.com/86412887/188853127-2662a6d7-b556-4f1b-8fb3-46959eeb05b2.png)

## Etc
If 'LockException' error occurs when you try to run Snakefile using command in the 'Run' section above: 
- First, execute this command: 'snakemake --unlock'
  - As a result, a message saying 'Unlocking working directory' will appear. It means that LockException error is solved.
- And then, execute the command in the 'Run' section above: 'snakemake -j 10'
