import re
from re import *

def soma_string(frase):
    res = re.split(r",", frase)
    soma = 0
    for r in res:
        soma += int(r)
    return soma

print(soma_string("4,10,-6,1,-9,-5, 5, 10"))