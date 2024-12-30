import re
from re import *

lista = [
    "4700-000",
    "1234-567",
    "8541-543",
    "4123-974",
    "9481-025"
]

pares = []

for l in lista:
    s = re.split(r"-", l)
    pares += [(s[0], s[1])]

print(pares)