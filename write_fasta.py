def write_fasta_list(filename, chromosome, sequence):
    #1 file, chromosome(array with n elements), sequence(array with n elements)
    f = open(filename,'w')
    for i in range(len(chromosome)):
        f.write('>'+chromosome[i]+"\n")
        #print(chromosome[i])
        f.write(sequence[i]+"\n")
        #print(sequence[i][1:5])
    f.close()
    
def write_fasta_line(filename, chromosome, sequence):
    #1 file, 1 chromosome, 1 sequence
    f = open(filename,'w')
    f.write('>'+chromosome+"\n")
    f.write(sequence+"\n")
    f.close()

def write_fastas_list(filename, chromosome, sequence):
    #filename(array with n elements), chromosome(array with n elements), sequence(array with n elements)
    for i in range(len(filename)):
        f = open(filename[i],'w')
        f.write('>'+chromosome[i]+"\n")
        f.write(sequence[i]+"\n")
    f.close()