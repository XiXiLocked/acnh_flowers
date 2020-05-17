from flower_data import flower_names, get_flower_data
from collections import Counter
import sys
from pprint import pprint

def Count_by_Colors():
   for f in flower_names:
        t,_,_= get_flower_data(f)
        cc = Counter()
        for c in t:
            cc[c.split()[0]] +=1
        cc.pop('-')
        print(f,"color count=",len(cc), ":",cc)

def get_Color_by_gene(flower,gene):
    print(flower,gene,get_flower_data(flower)[0][gene])

def get_mothers():
    get_Color_by_gene(flower_names[0],0b01010101)
    for f in flower_names[1:]:
        get_Color_by_gene(f,0b010101)
def get_seed_gene():
    for f in flower_names:
        print(f)
        t,_,_ = get_flower_data(f)
        for i,c in enumerate(t):
            if 'seed' in c:
                print(c, format(i,"#08b"))

if __name__ =='__main__':
    Count_by_Colors()

    # get_Color_by_gene(sys.argv[1], int(sys.argv[2],2))
    get_mothers()
    get_seed_gene()
    for i in [0,1,3]:
        for j in [0,1,3]:
            get_Color_by_gene('cosmos',i*4+j*16)
       
