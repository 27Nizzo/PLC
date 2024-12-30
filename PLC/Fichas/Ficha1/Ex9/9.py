import re 
from re import *


def underscores(frase):
    res = re.sub(r"\s+", "_", frase, count = 0)
    return res

print(underscores("Aqui temos   um belo   exemplo   de frase    completamente  maluca  !"))
