import pandas as pd
import numpy as np
import random
import os
import sys
import argparse
from read_dictionary import *

parser = argparse.ArgumentParser(description='Necessary parameters for methylation erosion simulation.')

parser.add_argument('--NumRegions', default=1000, type=int, help='Number of regions')
parser.add_argument('--SeqLength', default=50, type=int, help='Length of each sequence in sampled fasta file')
parser.add_argument('--Sherman_CH', default=77, type=int, help='Value of Sherman parameter -CH(--CH_conversion)')
parser.add_argument('--Sherman_e', default=1, type=int, help='Value of Sherman parameter -e(--error_rate)')
parser.add_argument('--Sherman_q', default=40, type=int, help='Value of Sherman parameter -q(--quality)')
parser.add_argument('--Sherman_script', required = True, type=str, help='Sherman script')
parser.add_argument('--SaveDir', required = True, type=str, help='Directory in which you want to save create fasta files')
parser.add_argument('--DefaultCG', default=0, type=int, help='background methylation level')
parser.add_argument('--Default_Working_Dir', required = True, type=str, help='Default working directory')
parser.add_argument('--RandomSeed', default=2022, type=int, help='Random seed to be used')

args = parser.parse_args()

outfile_name = os.path.join(args.SaveDir, 'run_sherman.log')
sys.stdout = open(outfile_name,'w')
    
os.chdir(args.Default_Working_Dir)
random.seed(args.RandomSeed)

if not os.path.exists(os.path.join(args.SaveDir, 'Sherman_result/')):
    os.makedirs(os.path.join(args.SaveDir, 'Sherman_result/'))

for i in range(args.NumRegions):
    if not os.path.exists(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/')):
        os.makedirs(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/'))
    if not os.path.exists(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/First/')):
        os.makedirs(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/First/'))
    if not os.path.exists(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Erosion/')):
        os.makedirs(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Erosion/'))
    if not os.path.exists(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Second/')):
        os.makedirs(os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Second/'))
    else:
        continue

txt_files=[]
colnames=[]
for (root, directories, files) in os.walk(args.SaveDir):
    for file in files:
        if '.txt' in file:
            if 'checkpoint' not in file:
                f_ = os.path.join(args.SaveDir, file)
                txt_files.append(f_)
                colnames.append(f_.split('.')[0].split('2')[1])

total_values = {}
for i, filename in enumerate(txt_files):
    _, values = read_dictionary(filename)
    total_values[colnames[i]] = values

cg_default = args.DefaultCG

if not os.path.exists(os.path.join(args.SaveDir, 'All_Merged/')):
    os.makedirs(os.path.join(args.SaveDir, 'All_Merged/'))
    
for i in range(args.NumRegions):
    print("Starting Region {}".format(i+1))
    first_n = total_values['first_n'][i]
    second_n = total_values['second_n'][i]
    erosion_n = total_values['erosion_n'][i]
    cg_conversion = total_values['erosion_level'][i]
    repl_num = total_values['repl_num'][i]
    current_region_first_dir = os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/First/')
    current_Sherman_first_dir = os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/First/')
    current_region_second_dir = os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Second/')
    current_Sherman_second_dir = os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Second/')
    current_region_erosion_dir = os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Erosion/')
    current_Sherman_erosion_dir = os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/Erosion/')
    
    first_sherman_cmd = args.Sherman_script + ' -l ' + str(args.SeqLength) + ' -n ' + str(first_n) \
    + ' --genome_folder ' + current_region_first_dir + ' -o ' + current_Sherman_first_dir + \
    ' -CG ' + str(args.DefaultCG) + ' -CH ' + str(args.Sherman_CH) + ' -e ' + str(args.Sherman_e) + ' -q ' + str(args.Sherman_q)
    
    second_sherman_cmd = args.Sherman_script + ' -l ' + str(args.SeqLength) + ' -n ' + str(second_n) \
    + ' --genome_folder ' + current_region_second_dir + ' -o ' + current_Sherman_second_dir + \
    ' -CG ' + str(args.DefaultCG) + ' -CH ' + str(args.Sherman_CH) + ' -e ' + str(args.Sherman_e) + ' -q ' + str(args.Sherman_q)
    
    erosion_sherman_cmd = args.Sherman_script + ' -l ' + str(args.SeqLength) + ' -n ' + str(erosion_n) \
    + ' --genome_folder ' + current_region_erosion_dir + ' -o ' + current_Sherman_erosion_dir + \
    ' -CG ' + str(cg_conversion) + ' -CH ' + str(args.Sherman_CH) + ' -e ' + str(args.Sherman_e) + ' -q ' + str(args.Sherman_q)
    
    print("\nFirst subregion sherman command: ")
    print(first_sherman_cmd)
    print("\nErosion subregion sherman command: ")
    print(erosion_sherman_cmd)
    print("\nSecond subregion sherman command: ")
    print(second_sherman_cmd)
    
    os.system(first_sherman_cmd)
    os.system(second_sherman_cmd)
    os.system(erosion_sherman_cmd)
    
    erosion_repl_fa = os.path.join(current_Sherman_erosion_dir, 'erosion_repl.fastq')
    erosion_repl_cmd = "cat " + current_Sherman_erosion_dir + "simulated.fastq >> " + erosion_repl_fa
    
    print("\nConcatenating Sherman results from erosion subregion for {} times...".format(repl_num))
    print(erosion_repl_cmd)
    
    for j in range(int(repl_num)):
        os.system(erosion_repl_cmd)

    merged_fastq = os.path.join(args.SaveDir, 'Sherman_result/Region'+str(i+1)+'/merged.fastq')
    merge_first_cmd = "cat " + current_Sherman_first_dir + "simulated.fastq >> " + merged_fastq
    merge_erosion_cmd = "cat " + current_Sherman_erosion_dir + "erosion_repl.fastq >> " + merged_fastq
    merge_second_cmd = "cat " + current_Sherman_second_dir + "simulated.fastq >> " + merged_fastq
    print("\n------------------------------------------------------------------")
    print("Merging all Sherman results from this region into merged fastq file...")
    print(merge_first_cmd)
    print(merge_erosion_cmd)
    print(merge_second_cmd)
    os.system(merge_first_cmd)
    os.system(merge_erosion_cmd)
    os.system(merge_second_cmd)

    region_merged_fastq = os.path.join(args.SaveDir, 'All_Merged/merged.fastq')
    
    merge_first_cmd_ = "cat " + current_Sherman_first_dir + "simulated.fastq >> " + region_merged_fastq
    merge_erosion_cmd_ = "cat " + current_Sherman_erosion_dir + "erosion_repl.fastq >> " + region_merged_fastq
    merge_second_cmd_ = "cat " + current_Sherman_second_dir + "simulated.fastq >> " + region_merged_fastq
    print("\n-----------------------------------------------------")
    print("Merging all sherman results from all regions into merged fastq file...")
    print(merge_first_cmd_)
    print(merge_erosion_cmd_)
    print(merge_second_cmd_)
    os.system(merge_first_cmd_)
    os.system(merge_erosion_cmd_)
    os.system(merge_second_cmd_)
    
    print("\nTotal number of simulated reads(50bp length) from Region {}: {}".format(i+1, int(first_n)+int(erosion_n)*int(repl_num)+int(second_n)))
    print("\n=================================================")
