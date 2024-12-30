import ply.lex as lex

# Identificação dos tokens
tokens = (
    'NUMBER',
    'PLUS',
    'TIMES',

)

# Especificação de cada token
t_PLUS = R'\+'

t_TIMES = R'\*' 

# 1º Opção: Oferece mais flexibilidade e controle sobre o processamento do token.
def t_NUMBER1(t):
    r'\d+'
    t.value = int(t.value)
    return t
'''
2º Opção: É mais simples, mas não permite manipulações adicionais no valor do mesmo
t_NUMBER2 = R'\d+'
'''
# Os caracteres que estão entre '' são ignorados
t_ignore = ' \t\n'

# Para definir o comportamento do token caso encontre um caracter ou sequencia de caracteres que não corresponde a nenhum token conhecido 

def t_error(t):
    print(f'Char ilegal {t.value[0]}')
    t.lexer.skip(1)


data = '''
3 + 4 * 10
  + -20 *2
'''

lexer.input(data)

while tok := lexer.token():
    print(tok)

lexer = lex.lex()
