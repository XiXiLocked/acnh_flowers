from itertools import product
from collections import Counter


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
            f.write("%s,%s,"%(l[0],l[1]))
            for c,p in l[2:]:
                f.write('%s %02d,'%(c,p))
            f.write('\n')

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


if __name__ == "__main__":
    crossing3_table()
    crossing4_table()
