import csv
from itertools import product
from collections import Counter
m = list(csv.reader(open('ACNH_ACNL Flower Genes - Roses.csv')))[1:]
t={'00':'00', '01':'01','10':'01', '11':'11'}
cross = { i+j: list(map(lambda x:t[x[0]+x[1]],product(*zip(*i),*zip(*j))))for i,j in product(['00','01','11'], ['00','01','11'])}

genetypes = [a+b+c+d for _,_,_,_,a,b,c,d,_ in m]

def crossing(gene_a, gene_b):
     cc = Counter()
     x0,y0,z0,w0     = gene_a[:2], gene_a[2:4], gene_a[4:6], gene_a[6:8]
     x1,y1,z1,w1 = gene_b[:2], gene_b[2:4], gene_b[4:6], gene_b[6:8]
     for x in cross[x0+x1]:
       for y in cross[y0+y1]:
         for z in cross[z0+z1]:
           for w in cross[w0+w1]:
               cc[x+y+z+w]+=1
     print(cc)

crossing('01010101','01010101')

  
