Blue_gene = 252
def bfs_crossing(flower,gene_num):
    gene_types = get_flower_genetype(flower)
    gene_fun = fun_parents_children(gene_num)

    gene_crossing_methods = {}
    for gene, color in enumerate(gene_types):
        if color != '-':
            if 'seed' in color:
                gene_crossing_methods[gene] = [(gene,gene,8,0)]
            else:
                gene_crossing_methods[gene] = []
    gene_count =  len(gene_types)
    duplicate_check = [[False for _ in range(gene_count)] for _ in range(gene_count)]
    exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]

    for generation in [1,2,3,4]:
        exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]
        print('generation' ,generation-1 , 'exists',len(exist_gene))
        print('crossing gen', generation)

        for genei in exist_gene:
            for genej in exist_gene:
                # skip half methods
                if genei>genej: continue
                if duplicate_check[genei][genej]:
                    continue
                duplicate_check[genei][genej] = True

                children = gene_fun(genei,genej)
                for gene,p in children:
                    if gene not in [genei, genej]:
                        gene_crossing_methods[gene].append((genei,genej,p,generation))


    return gene_crossing_methods,gene_types
                
def find_parents(target_gene, methods,genes, generation):
    prob =0
    parents = [ v for v in methods[target_gene] if v[3]<generation and  v[2]>=prob ]
    return sorted(parents, key = lambda x:x[2])

def print_parents(prefix, gene, methods, genes, generation=999):
    parents = find_parents(gene,methods, genes, generation)
    for pa,pb,prob,gen in parents[:20]:
        eprob = 2**(prob-6)
        print(prefix+'-', genes[gene]+"(%d)="%gene, genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb,gen, '%.1f%%'%(eprob*100))
        if "seed" not in genes[pa]:
            print_parents(prefix+"| ", pa,methods,genes, gen)
        if pa!=pb:
            if "seed" not in genes[pb]:
                print_parents(prefix+"| ", pb,methods,genes, gen)




def bfs_crossing_withprob(flower,gene_num, desired_prob):
    gene_types = get_flower_genetype(flower)
    gene_fun = fun_parents_children(gene_num)

    gene_crossing_methods = {}
    for gene, color in enumerate(gene_types):
        if color != '':
            if 'seed' in color:
                gene_crossing_methods[gene] = [(gene,gene,8,0)]
            else:
                gene_crossing_methods[gene] = []
    gene_count =  len(gene_types)
    duplicate_check = [[False for _ in range(gene_count)] for _ in range(gene_count)]
    exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]

    for generation in [1,2,3,4]:
        exist_gene = [gene for gene in gene_crossing_methods if len(gene_crossing_methods[gene])>0 ]
        print('generation' ,generation-1 , 'exists',len(exist_gene))
        print('crossing gen', generation)

        for genei in exist_gene:
            for genej in exist_gene:
                # skip half methods
                if genei>genej: continue
                if duplicate_check[genei][genej]:
                    continue
                duplicate_check[genei][genej] = True

                children = gene_fun(genei,genej)
                for gene,p in children:
                    if gene not in [genei, genej]:
                        if 2**(p-6) >=desired_prob: gene_crossing_methods[gene].append((genei,genej,p,generation))


    return gene_crossing_methods,gene_types

def print_parents_success(prefix, gene, methods, genes, generation=999):
    if 'seed' in genes[gene]:
        return True
    any_success =False
    parents = find_parents(gene,methods, genes, generation)
    for pa,pb,prob,gen in parents:
        eprob = 2**(prob-6)
        ta = print_parents_success(prefix+"| ", pa,methods,genes, gen)
        if ta:
            if pa==pb:
                print(prefix+'-', genes[gene]+"(%d)="%gene, genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb,gen, '%.1f%%'%(eprob*100))
                any_success= True
            else:
                tb = print_parents_success(prefix+"| ", pb,methods,genes, gen)
                if tb:
                    print(prefix+'-', genes[gene]+"(%d)="%gene, genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb,gen, '%.1f%%'%(eprob*100))
                    any_success= True
    return any_success


def gene_repr(gene, genes):
      return '%s(%d)'%(genes[gene],gene)

def print_methods(gene,method, genes):
   for i in method[gene]:
          print(gene_repr(gene,genes), '=', gene_repr(i[0],genes),'+', gene_repr(i[1],genes), i[2])
                

if __name__ == "__main__":
    import pickle
    # methods,genes = bfs_crossing_withprob('roses', 4, 0.0624)
    methods,genes = bfs_crossing_withprob('cosmos', 3, 0.25)
    # methods,genes = bfs_crossing('cosmos', 3)
    for i,c in enumerate(genes):
        # if c.lower()=='black':
        if 'seed' in c.lower():
          print(number_gene(i),c)
       

    # pickle.dump((methods,genes),open('gen.pkl','wb'))

    # methods, genes = pickle.load(open('gen.pkl','rb'))
    # Blue_gene= 252
    print('-'*20)
    # print_methods(60,methods,genes)
    # print_methods(61,methods,genes)
    print_parents("",60,methods,genes)
    
    # print_parents('',4, methods,genes,3)
    # print_parents('',Blue_gene, methods,genes)

    # parents = [ v for v in methods[Blue_gene] ]
    # parents.sort(key = lambda x:x[2])
    # for pa,pb,prob,gen in parents:
    #     print("Blue(%d) %.1f%%= "%(Blue_gene, 2**(prob-6)*100),  genes[pa]+"(%d)"%pa,genes[pb]+"(%d)"%pb)
    #     print_parents('',pa, methods,genes,gen)
    #     print_parents('',pb, methods,genes,gen)
    # print_parents_success("",Blue_gene,methods,genes)
    # print_parents_success("",60,methods,genes)
    # print_parents_success("",61,methods,genes)
  
