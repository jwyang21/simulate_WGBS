import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Necessary parameters for methylation erosion simulation.')

parser.add_argument('--RefGenomeDir', required = True, type=str, help='Directory of human reference genome hg38.fa')
parser.add_argument('--SaveDir', required = True, type=str, help='Directory in which you want to save create fasta files')
parser.add_argument('--Default_Working_Dir', required = True, type=str, help='Default working directory')

args = parser.parse_args()

outfile_name = os.path.join(args.SaveDir, 'run_bismark.log')
sys.stdout = open(outfile_name,'w')

BisulfiteGenomeDir = os.path.join(args.RefGenomeDir, 'Bisulfite_Genome/')
if not os.path.exists(os.path.join(BisulfiteGenomeDir)):
    bisulfite_genome_prep = "bismark_genome_preparation " + args.RefGenomeDir
    print("Bisulfite_Genome is not made. Making Bisulfite_Genome....\n")
    print(bisulfite_genome_prep)
    os.system(bisulfite_genome_prep)
    
merged_dir = os.path.join(args.SaveDir, 'All_Merged/')
os.chdir(merged_dir)  #Sherman 결과인 merged.fastq 파일이 있는 디렉토리에서 bismark 돌려야 함

#전체 RefGenome인 hg38.fa에 대한 BisulfiteGenomeDir을 사용해서, Merged.fastq에 대한 Bismark 돌리기
bismark_cmd1 = "bismark --genome "+ args.RefGenomeDir +" merged.fastq"
os.system(bismark_cmd1)

print("Bismark command 1(Run Bismark):")
print("\n")
print(bismark_cmd1)
print("\n") 

bismark_cmd2 = "bismark_methylation_extractor merged_bismark_bt2.bam"
os.system(bismark_cmd2)

print("Bismark command 2(bismark_methylation_extractor):")
print("\n")
print(bismark_cmd2)
print("\n")

bismark_cmd3= "bismark2report"
os.system(bismark_cmd3)
print("\n")
print(bismark_cmd3)
print("\n")

bismark_cmd4= "bismark2summary"
os.system(bismark_cmd4)
print("\n")
print(bismark_cmd4)
print("\n")

#bismark 끝나고, default working directory로 돌아오기
os.chdir(args.Default_Working_Dir)

#bismark 결과파일인 bam file을 sort해서 저장.
bismark_bam = os.path.join(merged_dir,'merged_bismark_bt2.bam')
bismark_bam_sorted = os.path.join(merged_dir,'merged_bismark_bt2_sorted.bam')
bam_sort_command = "samtools sort " + bismark_bam + " > " + bismark_bam_sorted
os.system(bam_sort_command)
print("Bam_sort_command: ", bam_sort_command) #debug
print("\n")
print("All_Region_Merged bam file(Bismark result) is sorted."+"\n")
print("Finish.")
