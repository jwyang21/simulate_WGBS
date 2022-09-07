def read_chr_len(fname):
    chromosome=[]
    chr_len=[]
    with open(fname) as file:
        for line in file:
            string_list = line.split()
            chromosome.append(str(string_list[0]).strip())
            chr_len.append(str(string_list[1]).strip())
    chr_to_len = dict(zip(chromosome, chr_len))
    del(chromosome)
    del(chr_len)
    return chr_to_len