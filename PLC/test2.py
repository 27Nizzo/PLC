
import re

print("----Filtro por numero de Telefone-------")

pattern_num = re.compile(r'\d*[.-]+\d*[.-]\d*')

with open('file.txt', 'r') as f:
    contents = f.read()

    matches = pattern_num.finditer(contents)

    for match in matches:
        print(match)

print("----Filtro por email-------")
pattern_email = re.compile(r'[a-zA-Z0-9.+]+@[a-zA-Z0-9.+]+\.[a-zA-Z]{2,}')

with open('file.txt', 'r') as f2:
    contents = f2.read()

    matches = pattern_email.finditer(contents)

    for match in matches:
        print(match)

print("----Filtro por Rua-------")

#pattern_rua = re.compile(r'\bRua\s+[A-Za-z]+\b')
pattern_rua = re.compile(r'\bRua:\s+[A-Za-z]+\s[A-Za-z]+.\s(nº\d+ | \d)')

with open('file.txt', 'r') as f3:
    contents = f3.read()

    matches = pattern_rua.finditer(contents)

    for match in matches:
        print(match)

print("-----Filtro para numeros entre 800-900-----")

pattern_num2 = re.compile(r'[89]00[.-]\d\d\d[.-]\d\d\d\d')

with open('file.txt', 'r') as f4:
    contents = f4.read()

    matches = pattern_num2.finditer(contents)

    for match in matches:
        print(match)


print("------Filtro para os 'at's'------")
# queremos filtrar todas as palavras que acabem em at menos a palavra 'bat'

pattern_at = re.compile(r'[^b]at')

with open('file.txt', 'r') as f5:
    contents = f5.read()

    matches = pattern_at.finditer(contents)

    for match in matches:
        print(match)

print("---Filtro para senhores-----")

pattern_m = re.compile(r'(Mr\.?')


with open('file.txt', 'r') as f6:
    contents = f6.read()

    matches = pattern_m.finditer(contents)

    for match in matches:
        print(match)