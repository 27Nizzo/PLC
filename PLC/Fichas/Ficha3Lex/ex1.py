import ply.lex as lex



'''
1) Definir uma analisador léxico que seja capaz de ler uma frase
e de identificar os seus componentes(palavras, virgulas, sinais
de pontuação).
'''

tokens = [
    'PALAVRAS',
    'VIRGULAS',
    'PONTO_INTERROGACAO',
    'PONTO_FINAL',
    'PONTO_EXCLAMACAO',
    'PONTO_VIRGULA',
    'DOIS_PONTOS'
]

def t_PALAVRAS(t):
    r'\w+'
    return t

t_VIRGULAS = r','
t_PONTO_INTERROGACAO = r'\?' 
t_PONTO_FINAL = r'\.'
t_PONTO_EXCLAMACAO = r'!'
t_PONTO_VIRGULA = r';'
t_DOIS_PONTOS = r':'


t_ignore = ' \t'

def t_NEW_LINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

data = '''
Isto é um exemplo 
de uma frase para ser 
lida pelo o meu analisador
léxico.
'''

lexer = lex.lex()
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)