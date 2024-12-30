import re

frase = "Ola aaa OLA123ola e tuOla--ola."


res = re.search( r'[^ ]+?(?i:ola)', frase )
print(res)
#print( len(res) )
