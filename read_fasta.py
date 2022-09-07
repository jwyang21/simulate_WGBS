import re

def read_fasta(fname):
    chromosome=[]
    sequence=[]
    with open(fname) as file:
        for line in file:
            header = re.search(r'^>\w+', line)
            if header:
                line = line.rstrip("\n")
                line = line.lstrip(">")
                chromosome.append(line)
            else:
                sequence.append(line.replace('\n','')) 
    chr_to_seq = dict(zip(chromosome, sequence))
    del(chromosome)
    del(sequence)
    return chr_to_seq