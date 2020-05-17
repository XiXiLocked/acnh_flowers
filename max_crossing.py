from flower_data import flower_names, get_flower_data

def get_rare_colors(genes):
    colors = set(genes)
    colors.discard('-')
    non_seed_color = set(colors)
    for i in colors:
        if 'seed' in i:
            non_seed_color.discard(i)
            non_seed_color.discard(i.split()[0])
    return non_seed_color

def oracle_gen():
    """
    calculate max probability for a color from colors other than it
    """
    list_oracle_crossing = []


    for f in flower_names:
        t, cross_fn, prob_fn = get_flower_data(f)
        non_seed_color = get_rare_colors(t)
        d = {}
        list_oracle_crossing.append((f,d))
        for rare in non_seed_color:
            max_p = 0.0
            for i,ci in enumerate(t):
                if ci=='-' or ci == rare:
                    continue
                for j,cj in enumerate(t):
                    if cj=='-' or cj ==rare:
                        continue
                    for g, p in cross_fn(i,j):
                        if t[g]==rare:
                            max_p = max(max_p, prob_fn(p))
            
            d[rare] = max_p
    return list_oracle_crossing
                        



if __name__ == "__main__":
    oracles = oracle_gen()
    from pprint import pprint
    pprint(oracles)
    trans_flower = {"Roses":"玫瑰", "Cosmos":"波斯菊","Hyacinths": "风信子",
             "Lilies":"百合", "Mums":"菊花", "Pansies":"三色堇",
             "Tulips":"郁金香", "Windflowers":"银莲花"}
    trans_color = {"Black":"黑", "Blue":"蓝", "Orange":"橙",
                   "Pink":"粉", "Purple":"紫","Blue":"蓝","Green":"绿"
    }

    for f,l in oracles:
        for c in l:
            print("%s%s|%d%%|"%(trans_color[c],trans_flower[f],int(l[c]*100)))