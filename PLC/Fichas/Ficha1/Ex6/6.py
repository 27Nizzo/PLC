import re
from re import *

frase = """Ola eu vou de certeza. Tu e ele, vêm?
        Eu não espero por vós.
        Eu estou com pressa, ele tem de vir, nós vamos andando!"""


def pronomes(frase):
    res = re.findall(r"(?i:eu|tu|ele|ela|nós|vós|eles)", frase)
    return res 


print(pronomes(frase))