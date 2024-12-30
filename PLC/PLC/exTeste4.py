import re
text = "LINHA COM ((1) marca) ([de]) SUCESSO[(13)] [a] ou (2)"
s = re.search(r'\[([aeiou]+|[1-9]+)\]', text)
if ( s ):
    print(s.group())
else:
    print("Falhou")
print(s)
 