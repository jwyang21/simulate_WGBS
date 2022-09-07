# simulate_WGBS

## Overview 
Sampling sequencing reads, running sherman and running bismark.           
Final result file (.bam) is used as simulated WGBS reads.

## Installation
conda env create -f simulate_wgbs.yaml
- This commands creates a conda environment which is needed to run the uploaded Snakefile.

## Input
hg38.fa
- a GRCh38 fasta file named 'hg38.fa' is needed.
- GRCh38 fasta file can be downloaded from NCBI.
  - GRCh38 download link (NCBI): https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.26/

## Run
snakemake -j 10
- This command runs the uploaded Snakefile.
- Of course, using any other number after '-j' option, specifying the number of CPU cores to be used, is available.

## Visualize DAG of Snakefile workflow
snakemake -j --dag | dot -Tpng -o dag.png 
- Reference: https://haje01.github.io/2020/04/21/snakemake-tutorial.html

## Result
Files in 'meth_erosion' folder.

## DAG visualization of Snakefile workflow: 
![dag](https://user-images.githubusercontent.com/86412887/188853127-2662a6d7-b556-4f1b-8fb3-46959eeb05b2.png)
- It is also available from the uploaded 'dag.png' file.

## Etc
If 'LockException' error occurs when you try to run Snakefile using command in the 'Run' section above: 
- First, execute this command: 'snakemake --unlock'
  - As a result, a message saying 'Unlocking working directory' will appear. It means that LockException error is solved.
- And then, execute the command in the 'Run' section above: 'snakemake -j 10'
