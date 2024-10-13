# import pandas as pd

'''
dados = pd.read_csv('emd.csv')
print(dados.head())
'''

import re

text1 = "O João da Maria foi à feira comprar 1kg de maçã por 2,50€."
text2 = "A Maria da João foi ao café e comprou 1 café por 0,60€ ao senhor António"
padrao_nome = r"[A-ZÀ-Ý][a-zà-ý]+"
nomes1 = re.findall(padrao_nome, text1)
nomes2 = re.findall(padrao_nome, text2)
print(nomes1)
print(nomes2)
print(len(nomes1))
print(len(nomes2))
