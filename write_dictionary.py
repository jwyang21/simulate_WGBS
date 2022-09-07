def write_dictionary(dictionary, fname):
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    with open(fname, 'w') as f:
        for i in range(len(keys)):
            f.write(str(keys[i])+'\t')
            f.write(str(values[i])+'\n')
    f.close()