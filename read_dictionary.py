import numpy as np

def read_dictionary(fname):
    f = open(fname, 'r')
    lines = f.readlines()
    f.close()
    index = np.array([lines[i].split('\t')[0] for i in range(len(lines))])
    value = np.array([lines[i].split('\t')[1].split('\n')[0] for i in range(len(lines))])
    return index, value