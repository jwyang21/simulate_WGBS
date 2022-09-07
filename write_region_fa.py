import argparse
import pandas as pd
import numpy as np
import os
from write_fasta import *

# README: Write fasta files of each subregion (i.e., first, erosion, second) of each region (i.e., region 1, region2, ... , region1000) based on 'region_info.csv' made by the very previous rule

parser = argparse.ArgumentParser(description='Necessary parameters for methylation erosion simulation.')

parser.add_argument('--NumRegions', default=1000, type=int, help='Number of regions')
parser.add_argument('--SaveDir', required = True, type=str, help='Directory in which you want to save create fasta files')
parser.add_argument('--Default_Working_Dir', required = True, type=str, help='Default working directory')

args = parser.parse_args()

#python script
if not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/')):
    os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/'))
for i in range(args.NumRegions):
    if not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/')):
        os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/'))
    elif not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/First/')):
        os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/First/'))
    elif not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Second/')):
        os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Second/'))
    elif not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Erosion/')):
        os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Erosion/'))
    elif not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Merged/')):
        os.makedirs(os.path.join(args.SaveDir, 'Region_Seq/Region'+str(i+1)+'/Merged/'))
    else:
        continue
        
region_info = pd.read_csv(os.path.join(args.SaveDir, 'region_info.csv'))
chr_list = region_info['chromosome'].values
seq_list = region_info['sequence'].values
fname_list = region_info['file'].values
write_fastas_list(fname_list, chr_list, seq_list)
