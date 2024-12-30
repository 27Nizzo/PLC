import ply.lex as lex

# Lista de tokens
tokens = [
    'NUMBER',       # Números inteiros
    'PLUS',         # +
    'MINUS',        # -
    'TIMES',        # *
    'DIVIDE',       # /
    'LPAREN',       # (
    'RPAREN',       # )
    'IDENTIFIER',   # Variáveis ou identificadores
]

# Palavras-chave reservadas
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
}

# Adicionar palavras-chave à lista de tokens
tokens += list(reserved.values())

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Ignorar espaços em branco
t_ignore = ' \t'

# Definir ações para os tokens mais complexos
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Converter o valor em inteiro
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verificar se é palavra-chave
    return t

# Definir regra para novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Gerar erro para caracteres inválidos
def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

# Criar o analisador léxico
lexer = lex.lex()

# Testar o analisador léxico
data = '''
if x + 10 > y while z - 2
'''

lexer.input(data)
for token in lexer:
    print(token)
