import ply.lex as lex

# Lista de tokens

tokens = [
    "PLUS", # + 
    "MINUS", # - 
    "TIMES", # * 
    "DIVIDE", # /
    "ASSIGN", # :=
    "LBRACKET", # (
    "RBRACKET", # )
    "SEMICOLON", # ;
    "GT", # >
    "LT", # <
    "EQ", # ==
    "GE", # >=
    "LE", # <= 
    "JUNGLE_DIFF", # '!=' 
    "INCREMENT", # ++
    "DECREMENT", # --
    "ID", #!  NAO ESQUECER: é o token que representa os nomes de variáveis, funções e outros no programa
    "INTEGER",
    "NUMBER",
    "NUMBER_REAL"
]


# Palavras-chave reservadas 

reserved = {

    "IF" : "if",
    "ELSE" : "else",
    "THEN" : "then", 
    "WHILE" : "while",
    "FUNCTION" : "function",
    "PLC" : "plc",
    "VAR" : "var",
    "BEGIN" : "begin",
    "END" : "end",
    "READ" : "read",
    "WRITE" : "write"  
}

tokens += list(reserved.values()) 



# Expressões regulares para tokens simples

t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_SEMICOLON = r'\;'
t_GT = r'\>'
t_LT = r'\<'
t_EQ = r'\=\='
t_GE = r'\>\='
t_LE = r'\<\='
t_JUNGLE_DIFF = r'\!\='
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_ASSIGN = r'\:\='


# Definição de tokens mais complexos 

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NUMBER_REAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_COMMENT(t):
    r'//.* | \*[\s\S]*?\*/'
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

t_ignore = '    \t'


def t_newline(t): 
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere Inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()


data = '''
PLC teste

var
    a = 10;
    b = 20;

begin
    read a;
    b := a + 1;
    write b;
end
'''


lexer.input(data)

for token in lexer:
    print(token)

