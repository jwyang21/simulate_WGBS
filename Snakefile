import re
import pandas as pd
import numpy as np
import random
import os
import sys
import argparse

'''
# snakemake commands
snakemake -j 10 # run this Snakefile
snakemake -j --dag | dot -Tpng -o dag.png # visualize DAG of this workflow
'''
NumRegions = 3 # for test 
#NumRegions = 1000 # original

regions = np.arange(1, NumRegions+1)
RandomSeed = 2022

# Arguments to be used in rule exclude_chr22xy
hg38 = '/data/project/jeewon/research/reference/hg38/hg38.fa'
SampledDir = '/data/project/jeewon/research/reference/hg38_sampled/'

# Arguments to be used in sample_50kb_revions_v[i].py
RefGenomeLen = '/data/project/jeewon/research/reference/hg38/hg38.fa.sizes'
RefGenome = '/data/project/jeewon/research/reference/hg38_sampled/hg38_wo_22XY.fa'
RegionLength = 50000
SeqLength = 50
Sherman_n = 25000
Default_Working_Dir = '/data/project/jeewon/research/metheor/metheor_snake_v3'
SaveDir = os.path.join(Default_Working_Dir, 'meth_erosion')

# Arguments to be used in both Sherman and Bismark
Sherman_CH = 77
Sherman_e = 1
Sherman_q = 40
Sherman_script = '/data/project/jeewon/research/metheor/metheor_snake_v3/Sherman/Sherman'
DefaultCG = 0

# Arguments to be used in Bismark only(not in Sherman)
RefGenomeDir = '/data/project/jeewon/research/reference/hg38/'

rule all: #Run bismark
    input:
        os.path.join(SaveDir, 'All_Merged', 'merged.fastq') #result file of rule run_sherman #'/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/All_Merged/merged.fastq'
    output:
        os.path.join(SaveDir, 'All_Merged', 'merged_bismark_bt2.bam') #'/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/All_Merged/merged_bismark_bt2.bam'
    threads: 10
    shell:
        'python3 {Default_Working_Dir}/run_bismark.py --RefGenomeDir {RefGenomeDir} --SaveDir {SaveDir} --Default_Working_Dir {Default_Working_Dir}'

rule exclude_chr22xy:
    input:
        hg38
    output:
        os.path.join(SampledDir, 'hg38_wo_22XY.fa')
    threads: 10
    shell:
        'python3 {Default_Working_Dir}/hg38_exclude_chr22xy.py --filename {hg38} --result_dir {SampledDir}'

rule sample_50kb_regions: 
    input:
        os.path.join(SampledDir, 'hg38_wo_22XY.fa') 
    output:
        os.path.join(SaveDir, 'region2chromosome.txt'),
        os.path.join(SaveDir, 'region2erosion_level.txt'),
        os.path.join(SaveDir, 'region2erosion_n.txt'),
        os.path.join(SaveDir, 'region2first_n.txt'),
        os.path.join(SaveDir, 'region2positive.txt'),
        os.path.join(SaveDir, 'region2repl_num.txt'),
        os.path.join(SaveDir, 'region2second_n.txt'),
        os.path.join(SaveDir, 'region_info.csv'),               
    threads: 10
    shell:
        'python3 {Default_Working_Dir}/sample_50kb_regions.py --RefGenomeLen {RefGenomeLen} --RefGenome {RefGenome} --RegionLength {RegionLength} --NumRegions {NumRegions} --SeqLength {SeqLength} --SaveDir {SaveDir} --Default_Working_Dir {Default_Working_Dir} --RandomSeed {RandomSeed}'
         
rule write_fa:
    input:
        os.path.join(SaveDir, 'region_info.csv') 
    output:
        first = expand('{d}/Region_Seq/Region{n}/First/first.fa', d=SaveDir, n=regions),
        erosion = expand('{d}/Region_Seq/Region{n}/Erosion/erosion.fa', d=SaveDir, n=regions),
        second = expand('{d}/Region_Seq/Region{n}/Second/second.fa', d=SaveDir, n=regions),
        merged = expand('{d}/Region_Seq/Region{n}/Merged/merged.fa', d=SaveDir, n=regions)
    threads: 10
    shell:
        'python3 {Default_Working_Dir}/write_region_fa.py --NumRegions {NumRegions} --SaveDir {SaveDir} --Default_Working_Dir {Default_Working_Dir}'

rule run_sherman:
    input:
        first = expand('/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/Region_Seq/Region{n}/First/first.fa', n=regions),
        erosion = expand('/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/Region_Seq/Region{n}/Erosion/erosion.fa', n=regions),
        second = expand('/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/Region_Seq/Region{n}/Second/second.fa', n=regions),
        merged = expand('/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/Region_Seq/Region{n}/Merged/merged.fa', n=regions)
    output: 
        '/data/project/jeewon/research/metheor/metheor_snake_v3/meth_erosion/All_Merged/merged.fastq'
    threads: 10
    shell:
        'python3 {Default_Working_Dir}/run_sherman.py --NumRegions {NumRegions} --SeqLength {SeqLength} --Sherman_CH {Sherman_CH} --Sherman_e {Sherman_e} --Sherman_q {Sherman_q} --Sherman_script {Sherman_script} --SaveDir {SaveDir} --DefaultCG {DefaultCG} --Default_Working_Dir {Default_Working_Dir} --RandomSeed {RandomSeed}' 
 
