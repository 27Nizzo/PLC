import ply.lex as lex

# Lista de tokens
class LexerPLC(object):
    tokens = [
        "PLUS", # + 
        "MINUS", # - 
        "TIMES", # * 
        "DIVIDE", # /
        "ASSIGN", # =
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
        "NUMBER_REAL",
        "STRING",
        "OR",
        "AND",
        "QUOTE",
        "FUNCTION"
    ]


    # Palavras-chave reservadas 

    reserved = {

        "if" : "IF",
        "else" : "ELSE",
        "then" : "THEN", 
        "while" : "WHILE",
        "plc" : "PLC",
        "var" : "VAR",
        "begin" : "BEGIN",
        "end" : "END",
        "read" : "READ",
        "write" : "WRITE",
        "return" : "RETURN",
        "for" : "FOR"
    }

    literals = [':','"']

    tokens += list(reserved.values()) 



    # Expressões regulares para tokens simples

    t_LBRACKET = r'\('
    t_RBRACKET = r'\)'
    t_SEMICOLON = r'\;'
    t_QUOTE = r'\"'
    t_GT = r'\>'
    t_LT = r'\<'
    t_EQ = r'\=\='
    t_GE = r'\>\='
    t_LE = r'\<\='
    t_JUNGLE_DIFF = r'\!\='
    t_OR = r'\|\|'
    t_AND = r'\&\&'
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'\-\-'

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_TIMES = r'\*'
    t_DIVIDE = r'\/'
    t_ASSIGN = r'\='


    # Definição de tokens mais complexos 

    def t_FUNCTION(self,t):
        r'fun(?=[ ])'
        return t

    def t_NUMBER(self,t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NUMBER_REAL(self,t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_STRING(self,t):
        r'(?<=\")[A-Za-z0-9\, !-()\?\-\:\\]*(?=\")'
        return t

    def t_COMMENT(self,t):
        r'//.* | \*[\s\S]*?\*/'
        pass

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    t_ignore = '    \t'


    def t_newline(self,t): 
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self,t):
        print(f"Caractere Inválido: {t.value[0]}")
        t.lexer.skip(1)

    def token(self):
        try:
            return next(self.token_stream)
        except StopIteration:
            return None

    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self.lexer = lex.lex(module=self, debug=debug, optimize=optimize, lextab=lextab, reflags=reflags)
        self.token_stream = None

    def input(self,s):
        self.lexer.input(s)
        self.token_stream = iter(self.lexer.token,None)

with open(f"teste3.plc") as f:
    content = f.read()

lexer = LexerPLC()
lexer.input(content)

for token in lexer.token_stream:
    print(f"({token.type} {repr(token.value)} {token.lineno})")