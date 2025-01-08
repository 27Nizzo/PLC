import ply.yacc as yacc
from analex import lexer,LexerPLC
import sys

tokens = LexerPLC.tokens

def p_programa(p):
    '''
    programa : plc
    '''
    p.parser.assembly = p[1]

def p_plc(p):
    '''
    plc : PLC ID VAR declaracoes comandos'''
    p[0] = f"START\n{p[4]}\n{p[5]}\nSTOP"

def p_declaracoes(p):
    '''
    declaracoes : declaracao 
                | declaracoes declaracao'''
    if len(p) == 1:
        p[0] = ""
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}\n{p[2]}"

def p_declaracao_vazia(p):
    '''
    declaracao : ID SEMICOLON 
    '''
    if p[1] not in p.parser.registos:
        p.parser.registos[p[1]] = p.parser.gp
        p.parser.gp += 1 
        p[0] = "PUSHI 0"
    else:
        print("Erro: Variável já inicializada")
        p.parser.success = False

def p_declaracao_numero(p):
    '''
    declaracao : ID ASSIGN NUMBER SEMICOLON 
    '''
    if p[1] not in p.parser.registos:
        p.parser.registos[p[1]] = p.parser.gp
        p.parser.gp += 1
        p[0] = f"PUSHI {p[3]}"
    else:
        print("Erro: Variável já inicializada")
        p.parser.success = False

def p_declaracao_leitura(p):
    '''
    declaracao : ID ASSIGN leitura 
    '''
    if p[1] not in p.parser.registos:
        p.parser.registos[p[1]] = p.parser.gp
        p.parser.gp += 1
        p[0] = f"PUSHI {p[3]}"
    else:
        print("Erro: Variável já inicializada")
        p.parser.success = False

def p_declaracao_funcao(p):
    '''
    declaracao : funcao
    '''
    p[0] = p[1]

def p_comandos(p):
    '''
    comandos : comando
             | comandos comando
    '''
    p[0] = "".join(p[1:])

def p_comando(p):
    '''
    comando : atribuicao
            | escrita
            | selecao
            | repeticao
            | call
            | incrementacao SEMICOLON
    '''
    p[0] = p[1]

def p_leitura(p):
    '''
    leitura : READ LBRACKET texto RBRACKET SEMICOLON
    '''
    p[0] = p[3]

# Implementação das expressões aritméticas

def p_atribuicao_expr(p):
    '''
    atribuicao : ID ASSIGN expressao SEMICOLON
    '''
    if p[1] in p.parser.registos:
        p[0] = f'{p[3]}STOREG {p.parser.registos.get(p[1])}\n'
    else:
        print(f"Erro, variável {p[1]} não definida.")
        p.parser.success = False

def p_atribuicao_leit(p):
    '''
    atribuicao : ID ASSIGN leitura
    '''
    if p[1] in p.parser.registos:
        p[0] = f'{p[3]}READ\nATOI\nSTOREG {p.parser.registos.get(p[1])}\n'
    else:
        print(f"Erro, variável {p[1]} não definida.")
        p.parser.success = False

def p_escrita(p):
    '''
    escrita : WRITE LBRACKET argumento RBRACKET SEMICOLON
    '''
    p[0] = p[3]

def p_argumento_texto(p):
    '''
    argumento : texto
    '''
    p[0] = p[1]

def p_argumento_expr(p):
    '''
    argumento : expressao
    '''
    p[0] = f'{p[1]}\nWRITEI\nWRITELN\n'

def p_texto(p):
    '''
    texto : QUOTE STRING QUOTE
    '''
    p[0] = f'PUSHS "{p[2]}"\nWRITES\nWRITELN\n'

def texto_vazio(p):
    '''
    texto : 
    '''
    p[0] = ''

def p_expressao(p):
    '''
    expressao : fator
              | expressao PLUS expressao
              | expressao MINUS expressao
              | expressao TIMES expressao
              | expressao DIVIDE expressao
              '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = f"{p[1]}{p[3]}\nADD\n"
    elif p[2] == '-':
        p[0] = f"{p[1]}{p[3]}\nSUB\n"
    elif p[2] == '*':
        p[0] = f"{p[1]}{p[3]}\nMUL\n"
    else:
        p[0] = f"{p[1]}{p[3]}\nDIV\n"

def p_fator(p):
    '''
    fator : ID
          | NUMBER 
          | LBRACKET expressao RBRACKET
    '''
    if p[1] == '(':
        p[0] = p[2]
    elif isinstance(p[1], str):
        p[0] = f"PUSHG {parser.registos[p[1]]}\n"
    else:
        p[0] = f"PUSHI {p[1]}\n"

def p_selecao(p): 
    '''
    selecao : IF LBRACKET condicao RBRACKET LCBRACKET comandos RCBRACKET
            | IF LBRACKET condicao RBRACKET LCBRACKET comandos RCBRACKET ELSE LCBRACKET comandos RCBRACKET'''
    
    #! NOTA: labels são marcadores no código assembly que indicam pontos especificos no programa para onde o fluxo de execução pode ser direcionado

    if len(p) == 8:
        # Condição if simples:

        label_fim = gerar_label()
        p[0] = f"{p[3]}\n"
        p[0] += f"JZ {label_fim}\n"
        p[0] += f"{p[6]}\n"
        p[0] += f"{label_fim}: NOP\n"
    else:
        # Comdição if-else:

        label_fim = gerar_label()
        p[0] = f'{p[3]}JZ {label_fim}\n{p[6]}JUMP {label_fim}f\n{label_fim}: NOP\n{p[10]}{label_fim}f: NOP\n'

def p_repeticao_for(p):
    '''
    repeticao : FOR LBRACKET declaracao condicao SEMICOLON incrementacao RBRACKET LCBRACKET comandos RCBRACKET
    '''
    label_inicio = gerar_label()
    label_fim = gerar_label()

    p[0] = f"{p[3]}\n{label_inicio}:\n{p[4]}\nJZ{label_fim}\n{p[9]}\n{p[6]}\nJUMP {label_inicio}\n{label_fim}:\n"

def p_repeticao_while(p):
    '''
    repeticao : WHILE LBRACKET condicao RBRACKET LCBRACKET comandos RCBRACKET
    '''
    label_inicio = gerar_label()
    label_fim = gerar_label()

    p[0] = f"{label_inicio}:\n"
    p[0] += f"{p[3]}\n"
    p[0] += f"JZ {label_fim}\n"
    p[0] += f"{p[6]}\n"
    p[0] += f"JUMP {label_inicio}\n"
    p[0] += f"{label_fim}:\n"

def p_incrementacao(p):
    '''
    incrementacao : ID INCREMENT
                  | ID DECREMENT
    '''
    if p[2] == '++':
        parser.registos[p[1]]
        p[0] = f"PUSHG {parser.registos[p[1]]}\nPUSHI 1\nADD\nSTOREG {parser.registos[p[1]]}\n"
        
    else:
        parser.registos[p[1]]
        p[0] = f"PUSHG {parser.registos[p[1]]}\nPUSHI 1\nSUB\nSTOREG {parser.registos[p[1]]}\n"
        

def p_condicao(p):
    '''
    condicao : condicao operador condicao
             | expressao
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]}{p[3]}{p[2]}'

condition_map ={
    ">": "SUP\n",
    "<": "INF\n",
    ">=": "SUPEQ\n",
    "<=": "INFEQ\n",
    "==": "EQUAL\n",
    "/=": "EQUAL\nNOT\n",
    "||": "ADD\nPUSHI 1\nSUPEQ\n",
    "&&": "ADD\nPUSHI 2\nSUPEQ\n",
}

def p_operador(p):
    '''
    operador  : GT
              | LT 
              | GE 
              | LE 
              | EQ 
              | JUNGLE_DIFF
              | OR
              | AND
    '''
    p[0] = f'{condition_map[p[1]]}'

    

# Função auxiliar para geral labels unicos:

cont_labels = 0

def gerar_label():
    global cont_labels
    cont_labels += 1
    return f"L{cont_labels}"

def p_funcao(p):
    '''
    funcao : FUNCTION ID LCBRACKET comandos RETURN expressao RCBRACKET SEMICOLON'''
    label_funcao = f"FUNC_{p[2]}"
    p[0] = f"JUMP {label_funcao}Ignore\n"
    p[0] += f"{label_funcao}:\n"
    p[0] += f"{p[4]}\n"
    p[0] += f"{p[6]}\n"

    p[0] += "RETURN\n"
    p[0] += f"{label_funcao}Ignore:"

    p.parser.funcoes[p[2]+"()"] = label_funcao

def p_chamadaF(p):
    '''call : ID LBRACKET RBRACKET SEMICOLON'''
    nome = p[1]+"()"
    if nome not in p.parser.funcoes:
        raise Exception(f"Função {p[1]} não declarada") #
    label_funcao = p.parser.funcoes[nome]
    p[0] = f"PUSHA {label_funcao}\n"
    p[0] += "CALL\n"
 

def p_error(p):
    if p:
        print(f"Erro de sintaxe: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do ficheiro")

precedence = (
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE")
)

lexer = LexerPLC()
parser = yacc.yacc(start="programa")

parser.assembly = ""
parser.registos = {}
parser.gp = 0
parser.success = True
parser.funcoes = {}



def compile(p):
    try:
        with open(f"tests/{sys.argv[1]}.plc") as f:
            content = f.read()

        result = p.parse(input=content, lexer=lexer)
        print(p.assembly)
        
        if p.success:
            print("Ficheiro lido com sucesso")
            with open(f'tests/{sys.argv[1]}.vm', 'w+') as f_out:
                f_out.write(parser.assembly)
                f_out.close()
            print("Código assembly gerado e guardado.")
        else:
            print("Erro ao gerar o código.")
            
        return result
        
    except FileNotFoundError:
        print(f"Erro: O ficheiro {sys.argv[1]} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao processar o ficheiro: {str(e)}")
        print(p.registos,p.funcoes)

if __name__ == "__main__":
    teste = "teste3.plc"
    compile(parser)
