import re
import ply.lex as lex

# Correção: tokens em vez de token e como lista
tokens = [
    "WORDS",
    "CURVERB",
    "CURVELB",
    "EQUAL",
]

# Correção: expressão regular para palavras
def t_WORDS(t):
    r'[a-zA-Z]+'
    return t

# Definição dos tokens simples
t_CURVERB = r'\)'
t_CURVELB = r'\('
t_EQUAL = r'='

# Correção: espaços em branco para ignorar
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere Inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar o lexer
lexer = lex.lex()

# Dados de teste
data = '''
a(z = alah)
'''

# Fornecer dados ao lexer
lexer.input(data)

# Correção: loop para obter tokens
while True:
    tok = lexer.token()  # Correção: token() em vez de token
    if not tok:
        break
    print(tok)
