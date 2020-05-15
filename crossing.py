from flower_data import get_flower_data
from itertools import product, combinations
from dataclasses import dataclass,field
from typing import List,Dict,Union
from collections import defaultdict
import pprint

@dataclass
class crossing_result:
    gene:Dict[int,float] #= field(repr=False)
    prob:float
    method:Union[set, str]
    parents:List #= field(repr=False)

def all_combination(a:list):
    a = list(a)
    # return [[i] for i in a]
    l = []
    # for count in range(min(1,len(a))):
    for count in range(len(a)):
        l.extend(list(combinations(a,count+1)))
    return l
        

def SplitResult(result:crossing_result,color_gene):
    group_color = defaultdict(list)
    for g in result.gene:
        color = color_gene[g].split()[0]
        group_color[color].append((g,result.gene[g]))
    color_prob= dict()
    for c in group_color:
        color_prob[c] = sum([p for g,p in group_color[c]])

    l = []
    for combi in all_combination(group_color.keys()):
        if len(combi)==1:
            clr = combi[0]
            a_group = crossing_result({},color_prob[clr],clr,[result])
            for g,p in group_color[clr]:
                a_group.gene[g]=p
        else:
            a_group = crossing_result({},0.0, set(combi),[result])
            for clr in combi:
                a_group.prob+= color_prob[clr]
                for g,p in group_color[clr]:
                    a_group.gene[g]=p
        
        l.append(a_group)
    return l


        


def crossing(flower):
    color_gene, gene_crossing_fun,prob_fun = get_flower_data(flower)
    

    parents_result = []
    for gene,color in enumerate(color_gene):
        if 'seed' in color :
            parents_result.append(crossing_result({gene:1.0},1.0,color,[]))
    
    results_methods = {}
    skip_i = -1
    for _ in range(2):
        print('parents', len(parents_result))
        children_gene = []
        # normal crossing
        for i,a in enumerate(parents_result):
            if i<skip_i: continue
            skip_i = i
            for j,b in enumerate(parents_result):
                # crossing is symmetric, skip half crossing results
                if i<j:break
                dd = {}
                for u,v in product(a.gene,b.gene):
                    prob = a.gene[u]*b.gene[v]
                    L_gene_prob = gene_crossing_fun(u,v)
                    for gene,p in L_gene_prob:
                        dd[gene] =dd.get(gene,0)+ prob*prob_fun(p)
                children_gene.append(crossing_result(dd,1.0,"crossing",[a,b]))
            # self duplication
            for u in a.gene:
                dd = {}
                L_gene_prob = gene_crossing_fun(u,u)
                for gene,p in L_gene_prob:
                    dd[gene]= prob_fun(p)
                children_gene.append(crossing_result(dd,1.0,"dup",[a]))

        gen_next = []
        for i in children_gene:
            gen_next.extend(SplitResult(i,color_gene))

        for k in gen_next:
            # only one color
            if  k.method is str:
                color = k.method
                t = results_methods.get(color,[])
                if len(t)<10:
                    t.append(k)
                    results_methods[color] = t

        parents_result.extend(gen_next)

    print(results_methods)

    # for i in results_methods:
    #     print(i)
    #     if i.lower()=='black':
    #         for line in results_methods[i]:
    #             pprint.pprint(line)



if __name__ == "__main__":
    crossing('cosmos')
