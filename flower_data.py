import csv
from make_table import encoding_gene, fun_parents_children
csvfiles =['csv/ACNH_ACNL Flower Genes - Roses.csv',
           #'csv/ACNH_ACNL Flower Genes - Carnations.csv',
           #'csv/ACNH_ACNL Flower Genes - Violets.csv',
           'csv/ACNH_ACNL Flower Genes - Cosmos.csv',
           'csv/ACNH_ACNL Flower Genes - Hyacinths.csv',
           'csv/ACNH_ACNL Flower Genes - Lilies.csv',
           'csv/ACNH_ACNL Flower Genes - Mums.csv',
           'csv/ACNH_ACNL Flower Genes - Pansies.csv',
           'csv/ACNH_ACNL Flower Genes - Tulips.csv',
           'csv/ACNH_ACNL Flower Genes - Windflowers.csv',]

flower_names = [v[29:-4] for v in csvfiles]

def get_flower_data(flower:str):
    if flower.lower() == 'roses':
        file = csvfiles[0]
        m = list(csv.reader(open(file)))[1:]
        genetypes_flower= ['-']*(4**4)
        for  _,_,_,_,a,b,c,d,color in m:
            idx = int(encoding_gene(a+b+c+d),16)
            genetypes_flower[idx] = color
        return genetypes_flower,fun_parents_children(4), lambda x:2.0**(x-8)
    # elif flower.lower() =='carnations':
    #     file = csvfiles[1]
    #     m = list(csv.reader(open(file)))[1:]
    #     genetypes_flower= ['-']*(2**4)
    #     for  _,_,_,a,b,color in m:
    #         idx = int(encoding_gene(a+b),16)
    #         genetypes_flower[idx] = color
    #     return genetypes_flower,fun_parents_children(2), lambda x:2.0**(x-4)
    # elif flower.lower() =='violets':
    #     file = csvfiles[2]
    #     m = list(csv.reader(open(file)))[1:]
    #     genetypes_flower= ['-']*(3**4)
    #     for  _,_,_,a,b,c,color in m:
    #         idx = int(encoding_gene(a+b+c),16)
    #         genetypes_flower[idx] = color
    #     return genetypes_flower,fun_parents_children(3), lambda x:2.0**(x-6)
    else:
        files = csvfiles[1:]
        for file in files:
            if flower.lower() in file.lower():
                m = list(csv.reader(open(file)))[1:]
                genetypes_flower = ['-'] * (4**3)
                for _,_,_,_,a,b,c,color in m:
                    idx = int(encoding_gene(a+b+c),16)
                    genetypes_flower[idx] = color
                return genetypes_flower,fun_parents_children(3), lambda x:2.0**(x-6)
    raise "no such flower"



