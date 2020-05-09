from itertools import product
from collections import Counter


def cross_pattern_one():
    t={'00':'00', '01':'01','10':'01', '11':'11'}
    cross = { i+j: list(map(lambda x:t[x[0]+x[1]],product(*zip(*i),*zip(*j))))for i,j in product(['00','01','11'], ['00','01','11'])}
    return cross

cross_pattern = cross_pattern_one()

def crossing3(gene_a, gene_b):
    cc = Counter()
    x0,y0,z0 = gene_a[:2], gene_a[2:4], gene_a[4:6]
    x1,y1,z1 = gene_b[:2], gene_b[2:4], gene_b[4:6]
    for v in product(cross_pattern[x0+x1],
                     cross_pattern[y0+y1],
                     cross_pattern[z0+z1]):
        gene_type = ''.join(v)
        cc[gene_type]+=1
    return cc

def crossing4(gene_a, gene_b):
    cc = Counter()
    x0,y0,z0,w0 = gene_a[:2], gene_a[2:4], gene_a[4:6], gene_a[6:8]
    x1,y1,z1,w1 = gene_b[:2], gene_b[2:4], gene_b[4:6], gene_b[6:8]
    for v in product(cross_pattern[x0+x1],
                     cross_pattern[y0+y1],
                     cross_pattern[z0+z1],
                     cross_pattern[w0+w1]):
        gene_type = ''.join(v)
        cc[gene_type]+=1
    return cc      

def crossing_table(genetypes, crossing_rules, filename):
    lines = []
    for parent_a in genetypes:
        for parent_b in genetypes:
            line = []
            children = crossing_rules(parent_a, parent_b)
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
    crossing_table(genetypes,crossing3, 'table3.csv')

def crossing4_table():
    genetypes = []
    gene = ['00', '01', '11']
    for v in product(*[gene]*4):
        gene_type = ''.join(v)
        genetypes.append(gene_type)
    crossing_table(genetypes,crossing4, 'table4.csv')


if __name__ == "__main__":
    crossing3_table()
    crossing4_table()
