import re
from re import *

def variavel_valida(var):
    return "Válida" if re.match(r'[a-zA-Z]\w*$', var) else "Inválido"

id0 = "Turma"
#id1  "_tot_"
id2 = "_tot_1.turma-2"
id3 = "tot_1.turma-2"
id4 = "tot_1_turma_2"
id5 = "tot1turma2"
XXXX = [id0] + [id2] + [id3] + [id4] + [id5]

for id in XXXX:
    print(variavel_valida(id))