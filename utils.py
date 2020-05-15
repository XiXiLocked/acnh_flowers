from flower_data import flower_names, get_flower_data
from collections import Counter
import sys

def Count_by_Colors():
   for f in flower_names:
        t,_= get_flower_data(f)
        cc = Counter()
        for c in t:
            cc[c.split()[0]] +=1
        cc.pop('-')
        print(f,cc,len(cc))

def get_Color_by_gene(flower,gene):
    print(flower,get_flower_data(flower)[gene])

def get_mothers():
    get_Color_by_gene(flower_names[0],0b01010101)
    for f in flower_names[1:]:
        get_Color_by_gene(f,0b010101)

if __name__ =='__main__':
    Count_by_Colors()

    # get_Color_by_gene(sys.argv[1], int(sys.argv[2],2))
    # get_mothers()

       
