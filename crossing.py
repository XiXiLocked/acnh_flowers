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
    def __repr__(self):
        if  'seed' in self.method:
            return self.method
        else:
            q = ",".join([crossing_result.__repr__(t) for t in self.parents])
            return "("+ str(self.method)+(" %.2f "%self.prob)+q +")"

def all_combination(a:list):
    a = list(a)
    l = []
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

def reducing_crossing(methods:List[crossing_result], color_genes):
    return methods

def reducing_dup(methods:List[crossing_result], color_genes):
    return methods

def reducing_last(methods:List[crossing_result],old:List[crossing_result], color_genes):
    seed_gene =set()
    for i,c in enumerate(color_genes):
        if 'seed' in c:
            seed_gene.add(i)
    filtered = []
    for result in methods:
        # discard low prob methods
        # if result.prob <0.1:
        #     continue

        if isinstance(result.method, str):
            if result.method =='dup':
                p = result.parents[0]
                if isinstance(p.method, set):
                    continue
                elif set(result.gene)<= set(p.parents[0].gene):
                        continue
                else:
                    filtered.append(result)
            elif result.method=='crossing':
                filtered.append(result)
            elif result.method=='seed':
                filtered.append(result)
            else:
                # the result is seed
                p = result.parents[0]
                if set(result.gene.keys()) <= seed_gene:
                    continue
                elif p.method=='crossing':
                    # same as dup
                    if len(p.parents[0].gene)==1 and set(p.parents[0].gene)== set(p.parents[1].gene):
                        continue
                    else:
                        filtered.append(result)
                elif p.method == 'dup':
                    # no new gene
                    if set(result.gene)<= set(p.parents[0].gene):
                        continue
                    else:
                        filtered.append(result)
                else:
                    filtered.append(result)
        else:
            # continue
            # if len(result.method)>2:
            #     continue
            # else:
                filtered.append(result)

    
    return filtered 

def pick_methods(methods:List[crossing_result],color_genes):
    colors = set(color_genes)
    colors.discard('-')
    seeds =  [ a for a in colors if 'seed' in a]
    for i in seeds:
        colors.discard(i)
        colors.discard(i.split()[0])
    
    print(colors)
    print('methods',len(methods))
    for clr in colors:
        for m in methods:
            if m.method == clr:
                print(m)


def crossing(flower, iterations):
    color_gene, gene_crossing_fun,prob_fun = get_flower_data(flower)

    parents_result = []
    for gene,color in enumerate(color_gene):
        if 'seed' in color :
            parents_result.append(crossing_result({gene:1.0},1.0,color,[]))
    
    skip_i = -1
    for _ in range(iterations):
        print('parents', len(parents_result))
        children_crossing = []
        children_dup = []
        for i,a in enumerate(parents_result):
            if i<skip_i: continue
            skip_i = i
            # normal crossing
            for j,b in enumerate(parents_result):
                # crossing is symmetric, skip half crossing results
                if i<j:break
                dd = {}
                for u,v in product(a.gene,b.gene):
                    prob = a.gene[u]*b.gene[v]
                    L_gene_prob = gene_crossing_fun(u,v)
                    for gene,p in L_gene_prob:
                        dd[gene] =dd.get(gene,0.0)+ prob*prob_fun(p)
                children_crossing.append(crossing_result(dd,1.0,"crossing",[a,b]))
            # self duplication
            dd = {}
            for u in a.gene:
                L_gene_prob = gene_crossing_fun(u,u)
                for gene,p in L_gene_prob:
                    dd[gene]= dd.get(gene,0.0)+prob_fun(p)*a.gene[u]
            children_dup.append(crossing_result(dd,1.0,"dup",[a]))

        children_crossing = reducing_crossing(children_crossing,color_gene)
        gen_next_crossing = []
        for i in children_crossing:
            gen_next_crossing.extend(SplitResult(i,color_gene))
        
        children_dup = reducing_dup(children_dup, color_gene)
        gen_next_dup = []
        for i in children_dup:
            gen_next_dup.extend(SplitResult(i,color_gene))

        gen_next = gen_next_dup+gen_next_crossing

        # remove inferior methods
        gen_next_filtered = reducing_last(gen_next,parents_result,color_gene)
        print(len(gen_next_filtered))
        parents_result.extend(gen_next_filtered)
    
    pick_methods(parents_result,color_gene)
        

if __name__ == "__main__":
    crossing('cosmos', 2)
