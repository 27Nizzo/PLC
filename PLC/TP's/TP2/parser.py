import ply.yacc as yacc
from analisadorLex import tokens

codigo = []

tabela_de_simbolos = {}


def p_programa(p):
    '''
    programa : PLC ID VAR declaracoes BEGIN comandos END'''
    p[0] = f"START\n{p[4]}\n{p[6]}\nSTOP"
    codigo.append(p[0])


def p_declaracoes(p):
    '''
    declaracoes : declaracao 
                | declaracoes declaracao'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}\n{p[2]}"

def p_declaracao(p):
    '''
    declaracao : ID SEMICOLON
               | ID EQ INTEGER SEMICOLON 
               | ID EQ leitura
    '''

    if len(p) == 3:
        tabela_de_simbolos[p[1]] = 0 
        p[0] = "PUSHI 0"
    else:
        tabela_de_simbolos[p[1]] = p[3]
        p[0] = f"PUSHI {p[3]}" 

# Implementação das expressões aritméticas

def p_expressao(p):
    '''
    expressao : termo
              | expressao PLUS termo
              | expressao MINUS termo'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = f"{p[1]}\n{p[3]}\nADD"
    else:
        p[0] = f"{p[1]}\n{p[3]}\nSUB"

def p_termo(p):
    '''
    termo : fator 
          | termo TIMES fator
          | termo DIVIDE fator'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = f"{p[1]}\n{p[3]}\nMUL"
    else:
        p[0] = f"{p[1]}\n{p[3]}\nDIV"

def p_fator(p):
    '''
    fator : ID
          | NUMBER 
          | LBRACKET expressao RBRACKET'''
    if p[1] == '(':
        p[0] = p[2]
    elif isinstance(p[1], str):
        p[0] = f"PUSHG {tabela_de_simbolos[p[1]]}"
    else:
        p[0] = f"PUSHI {p[1]}"

def p_selecao(p): 
    '''
    selecao : IF condicao ':' comandos END
            | IF condicao ':' comandos ELSE comandos END'''
    
    #! NOTA: labels são marcadores no código assembly que indicam pontos especificos no programa para onde o fluxo de execução pode ser direcionado

    if len(p) == 6:
        # Condição if simples:

        label_fim = gerar_label()
        p[0] = f"{p[2]}\n"
        p[0] += f"JZ {label_fim}\n"
        p[0] += f"{p[4]}\n"
        p[0] += f"{label_fim}:"
    else:
        # Comdição if-else:

        label_else = gerar_label()
        label_fim = gerar_label()
        p[0] = f"{p[2]}\n"
        p[0] += f"JZ {label_else}\n"
        p[0] += f"{p[4]}\n"
        p[0] += f"JUMP {label_fim}\n"
        p[0] += f"f{label_else}:\n"
        p[0] += f"{p[6]}\n"
        p[0] += f"{label_fim}:"

def p_repeticao(p):
    '''
    repeticao : WHILE condicao DO comandos END'''
    label_inicio = gerar_label()
    label_fim = gerar_label()

    p[0] = f"{label_inicio}:\n"
    p[0] += f"{p[2]}\n"
    p[0] += f"JZ {label_fim}\n"
    p[0] += f"JUMP {label_inicio}\n"
    p[0] += f"{label_fim}:"

def p_condicao(p):
    '''
    condicao : expressao operador expressao'''
    if p[2] == '>':
        p[0] = f"{p[1]}\n{p[3]}\nSUP"
    elif p[2] == '<':
        p[0] = f"{p[1]}\n{p[3]}\nINF"
    elif p[2] == '>=':
        p[0] = f"{p[1]}\n{p[3]}\nSUPEQ"
    elif p[2] == '<=':
        p[0] = f"{p[1]}\n{p[3]}\nINFEQ"
    elif p[2] == '==':
        p[0] = f"{p[1]}\n{p[3]}\nEQ"
    else:
        p[0] = f"{p[1]}\n{p[3]}\nNOTEQ"

    

# Função auxiliar para geral labels unicos:

cont_labels = 0

def gerar_label():
    global cont_labels
    cont_labels += 1
    return f"L{cont_labels}"

# TODO: Meter no relatorio:
'''
Esta implementação:

-> Gera código Assembly para estruturas IF e WHILE1

-> Usa labels para controle de fluxo

-> Implementa todas as comparações necessárias

-> Permite aninhamento das estruturas de controle1

-> Gera código otimizado para a máquina virtual VM
'''
        

# Implementar a funcionalidade escolhida subprogramas:

def p_funcao(p):
    '''
    funcao : FUNCTION ID INTEGER BEGIN comandos RETURN expressao SEMICOLON END'''
    label_funcao = f"FUNC_{p[2]}"
    p[0] = f"JUMP END_{label_funcao}\n"
    p[0] += f"{label_funcao}:\n"
    p[0] += f"{p[5]}\n"
    p[0] += f"{p[7]}\n"

    p[0] += "RETURN\n"
    p[0] += f"END_{label_funcao}:"

    tabela_simbolos[p[2]] = {
        'tipo' : 'funcao',
        'label' : label_funcao,
        'return' : 'INTEGER'
    }

def p_chamadaF(p):
    '''fator : ID LBRACKET RBRACKET'''
    if p[1] not in tabela_de_simbolos or tabela_de_simbolos[p[1]]['tipo'] != 'funcao':
        raise Exception(f"Função {p[1]} não declarada") #

    label_funcao = tabela_de_simbolos[p[1]]['label']
    p[0] = f"PUSHA {label_funcao}\n"
    p[0] += "CALL\n"


# TODO: Meter no relatório:
'''  
Esta implementação:

   -> Permite definir funções sem parâmetros que retornam inteiro
   
   -> Gera código Assembly apropriado para chamadas de função
   
   -> Gerencia o retorno de valores através da pilha
   
   -> Verifica se a função foi declarada antes do uso
   
   -> Usa labels únicos para cada função
   
   -> Permite que funções sejam usadas em expressões
'''


# Desenvolver a geração de codigo assembly para VM



# Criar um sistema de variáveis temporárias 
 



def p_error(p):
    if p:
        print(f"Erro de sintaxe: token inesperado '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe: fim inesperado do ficheiro")

parser = yacc.yacc()

def compile(data):
    result = parser.parse(data)
    return result