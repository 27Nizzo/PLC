import re 
from re import *

def troca_de_curso(frase, curso):
    res = re.sub(r'LEI', curso, frase, count = 0)
    return res

print(troca_de_curso("LEI é o melhor curso! Adoro LEI! Gostar de LEI devia ser uma lei.", "LCC"))
