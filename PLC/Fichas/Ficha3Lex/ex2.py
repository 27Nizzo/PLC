import ply.lex as lex

'''
2) Define um analisador léxico capaz de receber listas 
com números, palavras ou valores booleanos como input
(e.g.: `[ 1,5, palavra, False ,3.14,   0, fim]`) e 
identificar os seus *tokens*.
'''

tokens = (
    'NUMEROS',
    'PALAVRAS',
    'BOOLEANOS'
)

def t_NUMEROS(t):
  r'\d+(\.\d+)?'
  if '.' in t.value:
    t.value = float(t.value)
  else: 
    t.value = int(t.value)
  return t

def t_PALAVRAS(t):
  r'\w+'
  return t

def t_BOOLEANOS(t):
  r'True|False'
  t.value = True if t.value == 'True' else False
  return t

t_ignore = ' \t\n'

def t_new_line(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t):
  print(f"Caractere Inválido: {t.value[0]}")
  t.lexer.skip(1)

lexer = lex.lex()

data = '''
[1,5,palavra,False,3.14,0,fim]
'''

lexer.input(data)

while True:
  tok = lexer.token()
  if not tok:
    break
  print(tok)





