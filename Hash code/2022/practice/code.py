from functools import lru_cache
import sys
import pprint
from random import shuffle
from collections import defaultdict

sys.setrecursionlimit(10**9)

files = [
    'a_an_example',
    'b_basic',
    'c_coarse',
    'd_difficult',
    'e_elaborate'
]

C = 0

clients=[]
ingredient = set()

ingredient_freq = defaultdict(lambda:{'l':0,'d':0})

@lru_cache
def score(ingredients):
    n = 0
    for client in clients:
        like, dislike = client[0], client[1]
        
        ok = True
        for l in like:
            if not (l in ingredients):
                ok = False
                break
        if not ok: continue

        for d in dislike:
            if d in ingredients:
                ok = False
                break

        if ok:
            n += 1

    return n


@lru_cache
def maximise(ingredients):

    if len(ingredients)==0:
        return 0, ()
    max_score = score(ingredients), ingredients[:]

    if max_score[0]>1000: #target score
        return max_score

    for i in range(len(ingredients)):
        removed = list(ingredients[:])
        removed.pop(i)
        s = maximise(tuple(removed))

        if s[0]>max_score[0]:
            max_score = s

    return max_score

for file in files:   
    maximise.cache_clear()
    score.cache_clear()

    sys.stdin = open(file+'.in.txt')
    sys.stdout =open(file+'.out.txt', 'w')
    C = int(input())

    clients=[]
    ingredient = set()
    ingredient_freq = defaultdict(lambda:{'l':0,'d':0})

    for _ in range(C):
        preference =[]
        
        like = input().split()
        dislike = input().split()

        if len(like)>1:
            like = like[1:]
        else:
            like = []

        for l in like:
            ingredient_freq[l]['l'] += 1
            ingredient.add(l)

        preference.append(like)
        
        if len(dislike)>1:
            dislike = dislike[1:]
            
        else:
            dislike = []

        for d in dislike:
            ingredient_freq[d]['d'] += 1
            ingredient.add(d)
        
        preference.append(dislike)
        clients.append(preference)

    #heuristic
    for ing in ingredient_freq.keys():
        if ingredient_freq[ing]['l']<ingredient_freq[ing]['d']:
            ingredient.remove(ing)

    ingredient = tuple(ingredient)

    ans = maximise(ingredient)
    print(len(ans[1]), *ans[1])        