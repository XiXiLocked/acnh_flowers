import csv
from itertools import product
from collections import Counter
from pprint import pprint
t={'00':'00', '01':'01','10':'01', '11':'11'}
cross = { i+j: list(map(lambda x:t[x[0]+x[1]],product(*zip(*i),*zip(*j))))for i,j in product(['00','01','11'], ['00','01','11'])}


def crossing3(gene_a, gene_b):
     cc = Counter()
     x0,y0,z0 = gene_a[:2], gene_a[2:4], gene_a[4:6]
     x1,y1,z1 = gene_b[:2], gene_b[2:4], gene_b[4:6]
     for x in cross[x0+x1]:
       for y in cross[y0+y1]:
         for z in cross[z0+z1]:
               cc[x+y+z]+=1
     return cc

def crossing4(gene_a, gene_b):
     cc = Counter()
     x0,y0,z0,w0     = gene_a[:2], gene_a[2:4], gene_a[4:6], gene_a[6:8]
     x1,y1,z1,w1 = gene_b[:2], gene_b[2:4], gene_b[4:6], gene_b[6:8]
     for x in cross[x0+x1]:
       for y in cross[y0+y1]:
         for z in cross[z0+z1]:
           for w in cross[w0+w1]:
               cc[x+y+z+w]+=1
     return cc

m = list(csv.reader(open('csv/ACNH_ACNL Flower Genes - Roses.csv')))[1:]
genetypes_flower = {a+b+c+d:color for _,_,_,_,a,b,c,d,color in m}
genetypes = list(genetypes_flower)

not_assigned = 100
gen_of_genes =[not_assigned]*len(genetypes) 

# initialization
for i,g in enumerate(genetypes):
  if 'seed' in genetypes_flower[g]:
    gen_of_genes[i]=0


generation = 0
while gen_of_genes.count(not_assigned)>0:
  generation +=1
  print('breeding generation', generation)
  exist_gentype = [g for i,g in enumerate(genetypes) if gen_of_genes[i]!= not_assigned]
  for gi in exist_gentype:
      for gj in exist_gentype:
          children = crossing4(gi,gj)
          for k in children:
            idx = genetypes.index(k)
            gen_of_genes[idx] = min(generation,gen_of_genes[idx])
pprint([(g, genetypes_flower[g],gen_of_genes[i])   for i,g in enumerate(genetypes_flower)])#,  'gene of gen')

min_gen_of_color = set(j.split()[0] for j in genetypes_flower.values())
colorgen = {}
for i in min_gen_of_color:
  colorgen[i] = not_assigned

for i,g in enumerate(genetypes_flower):
  color = genetypes_flower[g].split()[0]
  gen = gen_of_genes[i]
  colorgen[color] = min(colorgen[color],gen)

print('minimun generation of flower color')
pprint(colorgen)




  
