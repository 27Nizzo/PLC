import re 
from re import *

def inteiros(frase):
    res = re.findall(r"-?\d+(?:[\.,]\d+)?", frase)
    return res

frase = "1.23dsds2,22-3-54ola+567"
print(inteiros(frase))