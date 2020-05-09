import csv
from itertools import product
from collections import Counter
from math import log2


def cross_pattern_one():
    t={'00':'00', '01':'01','10':'01', '11':'11'}
    gene = ['00','01','11']
    cross = {}
    for i,j in product(gene,gene):
        cross[i+j] =  [  t[x[0]+x[1]] for x in product(list(*zip(*i)), list(*zip(*j)))]
    return cross

cross_pattern = cross_pattern_one()

def split_gene(gene):
    return [gene[i:i+2] for i in range(0,len(gene),2)]

def encoding_gene(gene):
    return "%02x"%int(gene,2)

def crossing(gene_a, gene_b):
    cc = Counter()
    split_a = split_gene(gene_a)
    split_b = split_gene(gene_b)
    segments = [cross_pattern[a+b] for a,b in zip(split_a,split_b)]
    for v in product(*segments): 
        gene_type = ''.join(v)
        cc[gene_type]+=1
    return cc
 

def crossing_table(genetypes, filename):
    lines = []
    for parent_a in genetypes:
        for parent_b in genetypes:
            line = []
            children = crossing(parent_a, parent_b)
            line.append(parent_a)
            line.append(parent_b)
            for child in children:
                c = children[child]
                line.append((child, c))
            lines.append(line)

    with open(filename,'w') as f:
        for l in lines:
            f.write("%s,%s,"%(encoding_gene(l[0]),encoding_gene(l[1])))
            for c,p in l[2:]:
                f.write('%s %d,'%(encoding_gene(c),log2(p)))
            f.write('\n')
    

def extract_data(data):
    cp= data.split()
    return (int(cp[0],16),int(cp[1]))

def crossing3_table():
    genetypes = []
    gene = ['00', '01', '11']
    for v in product(*[gene]*3):
        gene_type = ''.join(v)
        genetypes.append(gene_type)
    crossing_table(genetypes, 'csv/table3.csv')

def crossing4_table():
    genetypes = []
    gene = ['00', '01', '11']
    for v in product(*[gene]*4):
        gene_type = ''.join(v)
        genetypes.append(gene_type)
    crossing_table(genetypes, 'csv/table4.csv')


def read_table(gene_num):
    if gene_num==3:
        file = 'csv/table3.csv'
    elif gene_num==4:
        file = 'csv/table4.csv'
    else:
        raise 'no such type'

    with open(file) as f:
        l = list(csv.reader(f))
        d = {}
        for v in l:
            parent_a = int(v[0],16)
            parent_b = int(v[1],16)
            d[parent_a*256+parent_b] = [extract_data(p) for p in v[2:-1]]
        return d


def fun_parents_children(gene_num):
    d = read_table(gene_num)
    return lambda a,b: d[a*256+b]

if __name__ == "__main__":
    crossing3_table()
    crossing4_table()
    