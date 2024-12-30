import re

text_to_search = '''
abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ

Ha Haha

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
123.555.1234

Mr. Schafer
Mr Smith 
Ms Davis
Mrs. Robinson 
Mr. T
'''

sentence = 'Start a sentence and then bring it to an end'

print(r'\tTab') # Raw string (r'qualquer coisa aqui dentro')

pattern = re.compile(r'abc')

matches = pattern.finditer(text_to_search)

for match in matches:
    print(match)

# Este for loop devolve: 
# re.Match object; span=(1, 4), match='abc'>
# Que significa que encontrou apenas uma sequencia de 'abc' no nosso texto, que vai do indice 1 até o indice 4

print(text_to_search[1:4])


pattern3 = re.compile(r'end$')

matches3 = pattern3.finditer(sentence)

for match3 in matches3:
    print(match3)

'''
MetaCharacters:

-> '.' : é um caracter especial que aceita todos os caracteres exceto "new line"(\n)

#! Nota: todos os caracteres em maiusculo são a negação do seu  caracter minúsculo

'''
print("Filtro para pessoas com Mr/Ms/Mrs:")
# pattern4 = re.compile(r'(Mr|Ms|Mrs)\.?\s[A-Z]\w*')
pattern4 = re.compile(r'\d{3}.\d{3}.\d{4}')

matches4 = pattern4.findall(text_to_search)

for match4 in matches4:
    print(match4)

print("Filtro:")

pattern5 = re.compile(r'start', re.I)

matches5 = pattern5.search(sentence)

print(matches5)


