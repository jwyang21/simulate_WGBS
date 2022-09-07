# simulate_WGBS

## Overview 
Sampling sequencing reads, running sherman and running bismark.           
Final result file (.bam) used as simulated WGBS reads

## Installation
conda env create -f simulate_wgbs.yaml

## Input
hg38.fa
- a GRCh38 fasta file named 'hg38.fa' is needed.
- GRCh38 fasta file can be downloaded from NCBI (link: https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/)

## Run
command to run Snakefile: snakemake -j 10

## Visualize DAG of Snakefile workflow
snakemake -j --dag | dot -Tpng -o dag.png (Ref: https://haje01.github.io/2020/04/21/snakemake-tutorial.html)

## Result
files in 'meth_erosion' folder

## Etc
If 'LockException' error occurs when you try to run Snakefile using command in the 'Run' section above: 
- First, execute this command: 'snakemake --unlock'
  - As a result, a message saying 'Unlocking working directory' will appear. It means that LockException error is solved.
- And then, execute the command in the 'Run' section above: 'snakemake -j 10'
