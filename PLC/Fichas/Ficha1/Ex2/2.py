import re 


def palavra_magica(frase):
    res = re.search(r"(?i:por favor)[,?!.]?$", frase)
    return "Válido" if res else "Inválido"

print(palavra_magica("Por favor, vem comigo!"))
print(palavra_magica("Posso ir à casa de banho, por favor?"))
print(palavra_magica("Necessito de um favor."))