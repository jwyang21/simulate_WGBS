import argparse
import random
import pandas as pd
import os
from read_fasta import *
from read_chr_len import *
from write_dictionary import *

parser = argparse.ArgumentParser(description='Necessary parameters for methylation erosion simulation.')

parser.add_argument('--RefGenomeLen', required = True, type=str, help='filename of reference genome length (of each chromosome)')
parser.add_argument('--RefGenome', required = True, type=str, help='filename of reference genome')
parser.add_argument('--RegionLength', default=50000, type=int, help='Length of each region')
parser.add_argument('--NumRegions', default=1000, type=int, help='Number of regions')
parser.add_argument('--Sherman_n', default=25000, type=int, help='Value of Sherman parameter -n(--number_of_seqs)')
parser.add_argument('--SeqLength', default=50, type=int, help='Length of each sequence in sampled fasta file')
parser.add_argument('--SaveDir', required = True, type=str, help='Directory in which you want to save create fasta files')
parser.add_argument('--Default_Working_Dir', required = True, type=str, help='Default working directory')
parser.add_argument('--RandomSeed', default=2022, type=int, help='Random Seed to be used')

args = parser.parse_args()


os.chdir(args.Default_Working_Dir)

if not os.path.exists(args.SaveDir):
    os.makedirs(args.SaveDir)
#if not os.path.exists(os.path.join(args.SaveDir, 'Region_Seq')):
#    os.makedirs(os.path.join(args.SaveDir, 'Region_Seq'))


random.seed(args.RandomSeed)

erosion_mask = [[False, True][random.random() < 0.5] for _ in range(args.NumRegions)] # positive_region
erosion_repl = [random.randint(2, 10) for _ in range(args.NumRegions)] # replicate_num for erosion subregion
erosion_cg = []
for i in range(args.NumRegions):
    if erosion_mask[i]:
        erosion_cg.append(random.randint(1,100))
    else:
        erosion_cg.append(0)

chr_to_len = read_chr_len(args.RefGenomeLen)

chr_all = list(chr_to_len.keys())
length_all = list(chr_to_len.values())

chr_exclude=['chr22','chrX','chrY']
chr_sampled = list(set(chr_all)-set(chr_exclude))
chr_len_sampled = dict([(key, chr_to_len[key]) for key in chr_sampled])

chr_to_seq = read_fasta(args.RefGenome)

region_chr_ind = [random.randint(1, len(chr_to_seq)) for _ in range(1000)]

region=[]
subregion=[]
chromosome=[]
start=[]
end=[]
seq=[]
gamma=[] #repl_num for erosion subregion
alpha=[] #sherman parameter CG-conversion for erosion subregion
frac=[]
positive_region=[]
file_list=[]
sherman_n=[]
region2chr={}
region2positive={}
region2erosion_level={}
region2repl_num={}

for i in range(args.NumRegions):
    subregion_start = ['0']
    subregion_end=[]
    chr_name = 'chr'+str(region_chr_ind[i])
    chr_len = int(chr_len_sampled[chr_name])
    chr_seq = chr_to_seq[chr_name]
    
    first_fasta = os.path.join(args.SaveDir,'Region_Seq/','Region'+str(i+1)+'/First/first.fa')
    erosion_fasta = os.path.join(args.SaveDir,'Region_Seq/','Region'+str(i+1)+'/Erosion/erosion.fa')
    second_fasta = os.path.join(args.SaveDir,'Region_Seq/','Region'+str(i+1)+'/Second/second.fa')
    merged_fasta = os.path.join(args.SaveDir,'Region_Seq/','Region'+str(i+1)+'/Merged/merged.fa')
    
    second_end = random.randint(args.RegionLength+1, chr_len)
    first_start = second_end - args.RegionLength
    region_seq = chr_seq[first_start:second_end]
    if 'N' in region_seq:
        while('N' in region_seq):
            second_end = random.randint(args.RegionLength+1, chr_len)
            first_start = second_end-args.RegionLength
            region_seq = chr_seq[first_start:second_end]
    
    erosion_start = random.randint(first_start, second_end) 
    if erosion_start-first_start<150 or second_end-erosion_start<500: # len(erosion subregion)+len(second subregion) should be >= 300bp. 500bp is quite enough to satisfy this.
        while erosion_start-first_start<150 or second_end-erosion_start<500:
            erosion_start = random.randint(first_start, second_end)
            
    erosion_end = random.randint(erosion_start, second_end)
    if second_end-erosion_end<150 or erosion_end-erosion_start<150: 
    # Both the length of second region and erosion region should be 150bp, which is long enough to cover sherman read length of 50bp.        
        while second_end-erosion_end<150 or erosion_end-erosion_start<150:
            erosion_end = random.randint(erosion_start, second_end)
            
    first_region = chr_seq[first_start:erosion_start]
    erosion_region = chr_seq[erosion_start:erosion_end]
    second_region = chr_seq[erosion_end:second_end]
    
    first_frac = float(len(first_region))/float(args.RegionLength)
    erosion_frac = float(len(erosion_region))/float(args.RegionLength)
    second_frac = float(len(second_region))/float(args.RegionLength)
    merged_frac = float(len(first_region)+len(erosion_region)+len(second_region))/float(args.RegionLength) #See if this equals 1.0
    
    erosion_read_n = args.Sherman_n/erosion_repl[i]
    first_sherman_n=int(round(args.Sherman_n*(first_frac)))
    erosion_sherman_n=int(round(erosion_read_n*erosion_frac))
    second_sherman_n=int(round(args.Sherman_n*(second_frac)))
    merged_sherman_n = first_sherman_n + (erosion_sherman_n * erosion_repl[i]) + second_sherman_n #check whether this equals args.Sherman_n

    current_region = 'region'+str(i+1)
    region.extend([current_region]*4)
    subregion.extend(["first","erosion","second","merged"])
    chromosome.extend([chr_name]*4)
    start.extend([first_start, erosion_start, erosion_end, first_start])
    end.extend([erosion_start, erosion_end, second_end, second_end])
    seq.extend([first_region, erosion_region, second_region, region_seq])
    gamma.extend(['',erosion_repl[i],'',''])
    alpha.extend(['',erosion_cg[i],'',''])
    frac.extend([first_frac, erosion_frac, second_frac, merged_frac])
    positive_region.extend(['',erosion_mask[i],'',''])
    file_list.extend([first_fasta, erosion_fasta, second_fasta, merged_fasta])
    sherman_n.extend([first_sherman_n, erosion_sherman_n, second_sherman_n, merged_sherman_n])
    region2chr[str('region'+str(i+1))]=chr_name
    region2positive[str('region'+str(i+1))]=erosion_mask[i]
    region2erosion_level[str('region'+str(i+1))] = erosion_cg[i]
    region2repl_num[str('region'+str(i+1))] = erosion_repl[i]
region_info=pd.DataFrame({'region':region, 'subregion':subregion, 'chromosome':chromosome, 'start':start, 'end':end, \
                          'positive_region':positive_region, 'alpha':alpha, 'gamma':gamma,'length_frac':frac, 'Sherman_n':sherman_n,'sequence':seq, 'file':file_list})

first_ = region_info[region_info['subregion']=='first']
erosion_ = region_info[region_info['subregion']=='erosion']
second_ = region_info[region_info['subregion']=='second']
first_n = first_['Sherman_n'].values
erosion_n = erosion_['Sherman_n'].values
second_n = second_['Sherman_n'].values
region2first_n = {}
region2erosion_n = {}
region2second_n = {}
for i in range(len(first_)):
    region2first_n[str('region'+str(i+1))] = first_n[i]
    region2erosion_n[str('region'+str(i+1))] = erosion_n[i]
    region2second_n[str('region'+str(i+1))] = second_n[i]
    
region_info.to_csv(os.path.join(args.SaveDir, 'region_info.csv'), index=False)
chromosome_dict_fname = os.path.join(args.SaveDir, 'region2chromosome.txt')
positive_dict_fname = os.path.join(args.SaveDir, 'region2positive.txt')
erosion_level_dict_fname = os.path.join(args.SaveDir, 'region2erosion_level.txt')
repl_num_dict_fname = os.path.join(args.SaveDir, 'region2repl_num.txt')
region2first_fname = os.path.join(args.SaveDir, 'region2first_n.txt')
region2second_fname = os.path.join(args.SaveDir, 'region2second_n.txt')
region2erosion_fname = os.path.join(args.SaveDir, 'region2erosion_n.txt')
write_dictionary(region2first_n, region2first_fname)
write_dictionary(region2second_n, region2second_fname)
write_dictionary(region2erosion_n, region2erosion_fname)
write_dictionary(region2chr, chromosome_dict_fname)
write_dictionary(region2positive, positive_dict_fname)
write_dictionary(region2erosion_level, erosion_level_dict_fname)
write_dictionary(region2repl_num, repl_num_dict_fname)
