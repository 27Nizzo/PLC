import re
from re import *

texto = """EU, dignissimo Eustáquio, disse: Eu não sei se deu, mas eu quero continuar a ser eu, Eufrásia.
Por eutro lado, eu ser eu é uma parte importante de qeum EU sou, mas não sou Deus."""

def narcissismo(frase):
    res = re.findall(r"(^(?i:eu)|\s(?i:eu))[\s.,!?;:]",frase)
    print(res)
    return len(res)

print(narcissismo(texto))