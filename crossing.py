from flower_data import get_flower_data
from itertools import product, combinations
from dataclasses import dataclass,field
from typing import List,Dict,Union
from collections import defaultdict
import pprint

@dataclass
class Crossing_Result:
    """
    stroing crossing methods.
    changing __repr__ to get better format.
    """
    gene:Dict[int,float] #= field(repr=False)
    prob:float
    method:str
    parents:List #= field(repr=False)
    def __repr__(self):
        if  'seed' in self.method:
            return self.method
        elif self.method=="crossing" :
            q = "\n    "+Crossing_Result.__repr__(self.parents[0])+',\n    '+Crossing_Result.__repr__(self.parents[1])
            gg = " "
            return "("+ self.method+ gg+q +")"
        elif self.method =="dup":
            q = ",".join([Crossing_Result.__repr__(t) for t in self.parents])
            gg = " "
            return "("+ self.method+ gg+q +")"
        else:
            q = ",".join([Crossing_Result.__repr__(t) for t in self.parents])
            gg = ''
            return "("+ self.method+gg+(" %.6f "%self.prob)+" "+q +")"


def SplitResult(result:Crossing_Result, color_geneX):
    """
    after crossing, you have a chance to move flowers of different colors
    for next crossing.
    this method groups flowers by color and calculates probability.
    """
    group_color = defaultdict(list)
    for g in result.gene:
        color = color_geneX[g]
        group_color[color].append((g,result.gene[g]))

    l = []
    for c in group_color:
        prob = 0.0
        d = {}
        for g,p in group_color[c]:
            prob+=p
            d[g]=p
        l.append(Crossing_Result(d,prob,c,[result]))

    return l

def has_color(color, result:Crossing_Result):
    if 'seed' in result.method:
        return color in result.method
    elif result.method == "crossing":
        return has_color(color, result.parents[0]) or has_color(color, result.parents[1])
    elif result.method == 'dup':
        return has_color(color, result.parents[0])
    else:
        # split result
        return result.method == color or has_color(color, result.parents[0])

def possibility_decreasing(result:Crossing_Result, prob= 0.0):
    if 'seed' in result.method:
        return True
    elif  result.method == "dup":
        return possibility_decreasing(result.parents[0],prob)
    elif result.method == "crossing":
        return possibility_decreasing(result.parents[0],prob) and possibility_decreasing(result.parents[1],prob)
    else:
        # split result
        return result.prob>= prob and possibility_decreasing(result.parents[0],result.prob/2)

def filtering_split(results:List[Crossing_Result],rare_colors: set, gene_record, color_record):
    for result in results:
        if not possibility_decreasing(result):
            continue
        # if result.method in rare_colors:
        #     p = result.parents[0]
        #     if p.method =='dup':
        #     # if has_color(result.method,result.parents[0]):
        #         # print("filtered ",result)
        #         if result.method ==p.method:
        #             continue

        for g in result.gene:
            gene_score = result.gene[g]
            if gene_score > gene_record[g][0]:
                gene_record[g][0] = gene_score
                gene_record[g][1] = [result]
            elif gene_score == gene_record[g][0]:
                gene_record[g][1].append(result)
        score = result.prob
        # for Blue roses only
        if result.method == "Blue":
            if score > color_record[result.method][0]:
                color_record[result.method][0] = score
                color_record[result.method][1] = [result]
            elif score > max(0.06, color_record[result.method][0]-0.03):
                color_record[result.method][1].append(result)
        else:
            if score > color_record[result.method][0]:
                color_record[result.method][0] = score
                color_record[result.method][1] = [result]
            elif score == color_record[result.method][0]:
                color_record[result.method][1].append(result)



def unique_accumulating(parents_result, pruning_gene_dict, pruning_color_dict, color_geneX):
    children_results = defaultdict(list)
    for g in pruning_gene_dict:
        results_g = pruning_gene_dict[g][1]
        children_results[color_geneX[g]].extend(results_g)

    for c in pruning_color_dict:
        results_c = pruning_color_dict[c][1]
        children_results[c].extend(results_c)
    for c in children_results:
        children = children_results[c]
        print(c, len(children))
        for i, methodi in enumerate(children):
            duplicated = False
            for j, methodj in enumerate(children):
                if i<=j:break
                if methodi.method == methodj.method and methodi.parents is methodj.parents:
                    duplicated = True
                    # print("duplicated!!", i,j,'\n',methodi,'\n', methodj)
                    break
            if not duplicated:
                parents_result.append(methodi)




def pick_methods(methods:List[Crossing_Result],rare_colors, f):
    """
    output searched methods
    """
    
    print("colors are", rare_colors)
    print('methods count ',len(methods))
    for clr in rare_colors:
        l :List[Crossing_Result]= []
        for m in methods:
            if m.method == clr:
                if not has_color(m.method,m.parents[0]):
                    l.append(m)
        l.sort(key=lambda x:x.prob, reverse=True)
        for i in l:
            f.write(str(i)+'\n')

def normal_crossing(a, b, color_geneX, gene_crossing_fun, prob_fun):
    l_gene_prob = [0.0]*len(color_geneX)
    for u,v in product(a.gene,b.gene):
        prob = a.gene[u]*b.gene[v]/(a.prob*b.prob)
        for gene,p in gene_crossing_fun(u,v):
            l_gene_prob[gene]+=prob_fun(p)*prob
    dd = {g:l_gene_prob[g] for g,c in enumerate(color_geneX) if c!= '-' and l_gene_prob[g]>0.0}
    crossing_rst = Crossing_Result(dd,1.0,"crossing",[a,b])
    l_crossing = SplitResult(crossing_rst, color_geneX)
    return l_crossing

def dup_crossing(a,color_geneX, gene_crossing_fun, prob_fun):
    l_gene_prob = [0.0]*len(color_geneX)
    for u in a.gene:
        for gene,p in gene_crossing_fun(u,u):
            prob = a.gene[u]/a.prob
            l_gene_prob[gene] += prob_fun(p)*prob
    dd = {g:l_gene_prob[g] for g,c in enumerate(color_geneX) if c!= '-' and l_gene_prob[g]>0.0}
    dup_result = Crossing_Result(dd,1.0,"dup",[a])
    l_dup = SplitResult(dup_result, color_geneX)
    return l_dup

    
def crossing(flower, iter_num, filename):
    """
    main function.
    simulating iter_num generations of crossing.
    the searching space is rather large, so some optimization is used.
    """
    color_gene, gene_crossing_fun,prob_fun = get_flower_data(flower)

    parents_result = []
    color_geneX = []

    rare_colors = set(color_gene)
    rare_colors.discard('-')
    for gene,color in enumerate(color_gene):
        if 'seed' in color :
            parents_result.append(Crossing_Result({gene:1.0},1.0,color,[]))
            rare_colors.discard(color)
            rare_colors.discard(color.split()[0])
        # remove seed
        color_geneX.append(color.split()[0])


    pruning_gene_dict = {g:[0.0,[]] for g,c in  enumerate(color_geneX) if c!= '-'}
    pruning_color_dict = {c:[0.0,[]] for c in  color_gene}

    skip_i = -1
    for _ in range(iter_num):
        print('new iter, parents', len(parents_result))
        for i in pruning_gene_dict:
            pruning_gene_dict[i][0]+=0.00001
            pruning_gene_dict[i][1].clear()
        for i in pruning_color_dict:
            pruning_color_dict[i][0]+=0.00001
            pruning_color_dict[i][1].clear()
        for i,a in enumerate(parents_result):
            if (i+1)%50 ==0:
                print("running", i)
            if i< skip_i : continue
            skip_i = i

            # normal crossing
            for j,b in enumerate(parents_result):
                # crossing is symmetric, skip half crossing results
                if i<j:break
                l_crossing = normal_crossing(a,b,color_geneX, gene_crossing_fun, prob_fun)
                filtering_split(l_crossing, rare_colors, pruning_gene_dict,pruning_color_dict)
                # from pprint import pprint
                # print(i,j,"crossing\t")
                # pprint(l_crossing)

            # self duplication
            # if len(a.gene)==1:
            #     continue
            l_dup = dup_crossing(a,color_geneX, gene_crossing_fun, prob_fun)
            filtering_split(l_dup, rare_colors, pruning_gene_dict, pruning_color_dict)
            # print(i,'-',"dup\t")
            # from pprint import pprint
            # pprint(l_dup)

        print("updated methods count", sum(
            (len(pruning_gene_dict[g][1]) for g in pruning_gene_dict ))+ sum(
                (len(pruning_color_dict[c][1]) for c in pruning_color_dict))
        )
        print("reducing!!!")
        old_parent_len = len(parents_result)
        unique_accumulating(parents_result, pruning_gene_dict, pruning_color_dict, color_geneX)
        print("reduced!!!", len(parents_result)-old_parent_len)
    print(flower)
    with open(filename,'w') as f:
        pick_methods(parents_result,rare_colors, f)
        

if __name__ == "__main__":
    print("Happy flowering")
    crossing('cosmos', 3,"results/cosmos.txt")
    crossing('hyacinths', 3,"results/hyacinths.txt")
    crossing('lilies', 3,"results/lilies.txt")
    crossing('mums', 3,"results/mums.txt")
    crossing('pansie', 3,"results/pansies.txt")
    crossing('tulip', 3,"results/tulips.txt")
    crossing('wind', 3,"results/windflowers.txt")
    crossing('roses', 4,"results/roses.txt")