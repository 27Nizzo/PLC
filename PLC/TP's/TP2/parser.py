import ply.yacc as yacc
from analex import lexer,LexerPLC

tokens = LexerPLC.tokens

def p_programa(p):
    '''
    programa : plc
    '''
    parser.assembly = {p[1]}

def p_plc(p):
    '''
    plc : PLC ID declaracoes BEGIN comandos END'''
    p[0] = f"START\n{p[4]}\n{p[6]}\nSTOP"

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

def p_declaracao(p):
    '''
    declaracao : ID SEMICOLON
               | ID ASSIGN NUMBER SEMICOLON
               | ID ASSIGN leitura
               | ASSIGN STRING SEMICOLON 
    '''
    # o ASSIGN STRING SEMICOLON lida com situações quando definimos strings em vars.


    if len(p) == 3:
        parser.registos[p[1]] = 0 
        p[0] = "PUSHI 0"
    elif len(p) == 5:
        if isinstance(p[3], int):
            parser.registos[p[1]] = p[3]
            p[0] = f"PUSHI {p[3]}"
        else:
            string_val = p[3][1:-1]
            parser.registos[p[1]] = string_val
            p[0] = f"PUSHS {p[3]}"
    else:
        parser.registos[p[1]] = p[3]
        p[0] = f"PUSHI {p[3]}"

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
    '''
    p[0] = p[1]

def p_leitura(p):
    '''
    leitura : READ LBRACKET texto RBRACKET SEMICOLON
    '''
    p[0] = f'{p[3]}'

# Implementação das expressões aritméticas

def p_atribuicao_expr(p):
    '''
    atribuicao : ID ASSIGN expressao SEMICOLON
    '''
    if p[1] in p.parser.registos:
        p[0] = f'{p[3]}STOREG {p.parser.registos.get(p[1])}\n'
    else:
        print(f"Erro, variável {p[1]} não definida.")
        parser.success = False

def p_atribuicao_leit(p):
    '''
    atribuicao : ID ASSIGN leitura SEMICOLON
    '''
    if p[1] in p.parser.registos:
        p[0] = f'{p[3]}READ\nATOI\nSTOREG {p.parser.registos.get(p[1])}\n'
    else:
        print(f"Erro, variável {p[1]} não definida.")
        parser.success = False

def p_escrita(p):
    '''
    escrita : WRITE LBRACKET argumento RBRACKET SEMICOLON
    '''
    p[0] = p[1]

def p_argumento_texto(p):
    '''
    argumento : texto
    '''
    p[0] = p[1]

def p_argumento_expr(p):
    '''
    argumento : expressao
    '''
    p[0] = f'{p[1]}WRITEI\nWRITELN\n'

def p_texto(p):
    '''
    texto : '"' STRING '"'
    '''
    p[0] = f'PUSHS "{p[2]}"\nWRITES\n'

def texto_vazio(p):
    '''
    texto : 
    '''
    p[0] = ''

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
        p[0] = f"PUSHG {parser.registos[p[1]]}"
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

def p_repeticao_for(p):
    '''
    repeticao : FOR LBRACKET declaracao SEMICOLON condicao SEMICOLON incrementacao RBRACKET ':' comando END
    '''
    label_inicio = gerar_label()
    label_fim = gerar_label()

    p[0] = f"{p[3]}\n{label_inicio}:\n{p[5]}\nJZ{label_fim}\n{p[10]}\n{p[7]}\nJUMP {label_inicio}\n{label_fim}:"

def p_repeticao_while(p):
    '''
    repeticao : WHILE LBRACKET condicao RBRACKET ':' comandos END
    '''
    label_inicio = gerar_label()
    label_fim = gerar_label()

    p[0] = f"{label_inicio}:\n"
    p[0] += f"{p[2]}\n"
    p[0] += f"JZ {label_fim}\n"
    p[0] += f"JUMP {label_inicio}\n"
    p[0] += f"{label_fim}:"

def p_incrementacao(p):
    '''
    incrementacao : ID INCREMENT
                  | ID DECREMENT
    '''
    if p[2] == '++':
        parser.registos[p[1]] += 1
        p[0] = f"PUSHG {parser.registos[p[1]]}\nPUSHI 1\nADD\nSTOREG {parser.registos[p[1]]}\n"
        
    else:
        parser.registos[p[1]] -=1
        p[0] = f"PUSHG {parser.registos[p[1]]}\nPUSHI 1\nSUB\nSTOREG {parser.registos[p[1]]}\n"
        

def p_condicao(p):
    '''
    condicao : expressao operador expressao
    '''
    p[0] = f'{p[1]}{p[3]}{p[2]}'

condition_map ={
    ">": "SUP\n",
    "<": "INF\n",
    ">=": "SUPEQ\n",
    "<=": "INFEQ\n",
    "==": "EQUAL\n",
    "/=": "EQUAL\nNOT\n",
    "or": "ADD\nPUSHI 1\nSUPEQ\n",
    "and": "ADD\nPUSHI 2\nSUPEQ\n",
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
    p[0] = f'{condition_map(p[1])}'

    

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
    if p[1] not in parser.registos or parser.registos[p[1]]['tipo'] != 'funcao':
        raise Exception(f"Função {p[1]} não declarada") #

    label_funcao = parser.registos[p[1]]['label']
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

lexer = LexerPLC()
parser = yacc.yacc(start="programa")

parser.assembly = ""
parser.registos = {}
parser.success = True



def compile(filename):
    try:
        with open(filename, 'r') as file:
            input_text = file.read()

        result = parser.parse(input=input_text, lexer=lexer)
        print(parser.assembly)
        
        if parser.success:
            print("Ficheiro lido com sucesso")
            output_filename = filename.replace('.plc', '.vm')
            with open(output_filename, 'w+') as f_out:
                f_out.write(parser.assembly)
                f_out.close()
            print("Código assembly gerado e guardado.")
        else:
            print("Erro ao gerar o código.")
            
        return result
        
    except FileNotFoundError:
        print(f"Erro: O ficheiro {filename} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao processar o ficheiro: {str(e)}")

if __name__ == "__main__":
    teste = "teste.plc"
    compile(teste)
