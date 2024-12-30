import re 
from re import *

# Exercicio 1:
print("---Exercicio 1:---")


def iso_8601(texto):
    res = re.sub(r"(\d{2})/(\d{2})/(\d{4})",r"\3-\2-\1", texto)
    return res


texto = """A 03/01/2022, Pedro viajou para a praia com a sua família.
Eles ficaram hospedados num hotel e aproveitaram o sol e o mar durante toda a semana.
Mais tarde, no dia 12/01/2022, Pedro voltou para casa e começou a trabalhar num novo projeto.
Ele passou muitas horas no escritório, mas finalmente terminou o projeto a 15/01/2022."""

print(iso_8601(texto))

# Exercicio 2:
print('\n')
print("---Exercicio 2:---")

file_names = [
  "document.txt", # válido
  "file name.docx", # inválido
  "image_001.jpg", # válido
  "script.sh.tt", # válido
  "test_file.txt", # válido
  "file_name.", # inválido
  "my_resume.docx", # válido
  ".hidden-file.txt", # válido
  "important-file.text file", # inválido
  "file%name.jpg" # inválido
]

def check_file(lista):
    results = []
    for l in lista: 
        res = re.match(r"^[\w\.\-]+\.[a-z]{1,4}$", l)
        results.append("Válido" if res else "Inválido")
    return results

print(check_file(file_names))

#Exercicio 3:
print('\n')
print("---Exercicio 3:---")

def filtro_nome(texto):
    nome = r'[A-Z][a-zéêãâàáõôóíú]+'
    res = re.sub(rf'({nome})(\s+{nome})+', r'\2 \1', texto)
    return res

texto = """Este texto foi feito por Sofia Guilherme Rodrigues Dos Santos, com
base no texto original de Pedro Rafael Paiva Moura, com a ajuda
dos professores Pedro Rangel Henriques e José João Antunes Guimarães Dias De Almeida.
Apesar de partilharem o mesmo apelido, a Sofia não é da mesma família do famoso
autor José Rodrigues  Santos."""

print(filtro_nome(texto))


#Exercicio 4:
print('\n')
print("---Exercicio 4:---")


def codigos_postais(lista):
    results = []
    for l in lista:
        res = re.match(r'^(\w+)-(\w+)$', l)
        if res:
            results.append((res.group(1), res.group(2)))
    return results

lista = [
    "4700-000", # válido
    "4715-012", # válido
    "987-6543", # inválido
    "1234-567", # válido
    "8x41-5a3", # inválido
    "84234-12", # inválido
    "4583--321", # inválido
    "4583-321", # válido
    "9481-025" # válido
]

print(codigos_postais(lista))

#Exercicio 5:
print('\n')
print("---Exercicio 5:---")

abreviaturas = {
    "UM": "Universidade do Minho",
    "LEI": "Licenciatura em Engenharia Informática",
    "UC": "Unidade Curricular",
    "PL": "Processamento de Linguagens",
    "MV" : "Maria Vitória",
    "mt" : "muito",
    "tb" : "também",
    "mb" : "muito bem",
    "cqd" : "como queriamos demonstrar"
}

texto1 = "A /UU de /PL é muito fixe! É uma /UC que acrescenta muito ao curso de /LEI da /UM."
texto2 = """
- Eu gosto /mt de manga.
- Fixe! Eu e /tu /tb!
Fim da história /MV.
   /cqd.
   /mb para terminar!
"""
texto = texto1+"\n"+texto2

def expande(pal):
    def replace_abbr(match):
        abbr = match.group(1)
        return abreviaturas.get(abbr, match.group(0))
    
    return re.sub(r'/(\w+)', replace_abbr, pal)

print(expande(texto)) 


#Exercicio 6:
print('\n')
print("---Exercicio 6:---")

matriculas = [
    "AA-AA-AA", # inválida
    "LR-RB-32", # válida
    "1234LX", # inválida
    "PL 22 23", # válida
    "ZZ-99-ZZ", # válida
    "54-tb-34", # inválida
    "12 34 56", # inválida
    "42-HA BQ" # válida, mas inválida com o requisito extra
]


def matricula_valida(matricula):
    padrao = re.compile(r'^(?:[A-Z]{2}-[A-Z]{2}-\d{2}|\d{2}-[A-Z]{2}-\d{2}|\d{2} [A-Z]{2} \d{2}|[A-Z]{2} \d{2} \d{2})$')
    return bool(padrao.match(matricula))

# Testando a função com a lista de matrículas
for matricula in matriculas:
    print(f"{matricula}: {'válida' if matricula_valida(matricula) else 'inválida'}")



#Exercicio 7:
print('\n')
print("---Exercicio 7:---")
def substitui(texto):
    placeholders = re.findall(r'\[(.*?)\]', texto)
    for placeholder in placeholders:
        user_input = input(f"Por favor, insira um(a) {placeholder.lower()}: ")
        texto = re.sub(rf'\[{placeholder}\]', user_input, texto, 1)
    return texto

texto = """Num lindo dia de [ESTAÇÃO DO ANO], [NOME DE PESSOA] foi passear com o seu [EXPRESSÃO DE PARENTESCO MASCULINA].
Quando chegaram à [NOME DE LOCAL FEMININO], encontraram um [OBJETO MASCULINO] muito [ADJETIVO MASCULINO].
Ficaram muito confusos, pois não conseguiam identificar a função daquilo.
Seria para [VERBO INFINITIVO]? Tentaram perguntar a [NOME DE PESSOA FAMOSA], que também não sabia.
Desanimados, pegaram no objeto e deixaram-no no [NOME DE LOCAL MASCULINO] mais próximo.
Talvez os [NOME PLURAL MASCULINO] de lá conseguissem encontrar alguma utilidade para aquilo."""

substitui(texto)

#Exercicio 8:
print('\n')
print("---Exercicio 8:---")

def removeRep(frase):
  padrao = re.compile(r"\b(\w+)\b(?:\s+\1\b)+", re.IGNORECASE)
  frase_sem_rep = padrao.sub(r'\1', frase)
  print("Frase ínicial:")
  print(frase)
  print("\n")
  print("Frase sem Repetições:")
  print(frase_sem_rep)
    
frase = "Esta é uma uma frase frase frase com com palavras palavras repetidas repetidas."
print(removeRep(frase))



#Exercicio 9:
print('\n')
print("---Exercicio 9:---")




#Exercicio 10:
print('\n')
print("---Exercicio 10:---")


# Tabela de símbolos terminais e seus códigos
tokens = {
    'def': 1,
    'int': 2,
    'str': 3,
    'return': 4,
    '(': 5,
    ')': 6,
    '{': 7,
    '}': 8,
    ',': 9,
    '=': 10,
    '+': 11,
}

# Expressões regulares para identificar tokens
token_regex = [
    (r'\bdef\b', 1),
    (r'\bint\b', 2),
    (r'\bstr\b', 3),
    (r'\breturn\b', 4),
    (r'\(', 5),
    (r'\)', 6),
    (r'\{', 7),
    (r'\}', 8),
    (r',', 9),
    (r'=', 10),
    (r'\+', 11),
    (r'\b\d+\b', 13),  # números
    (r'\b[a-zA-Z_]\w*\b', 12),  # identificadores
]

def analisador_lexico(codigo):
    pos = 0
    tokens_encontrados = []
    while pos < len(codigo):
        match = None
        for token_expr in token_regex:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(codigo, pos)
            if match:
                text = match.group(0)
                tokens_encontrados.append((text, tag))
                pos = match.end(0)
                break
        if not match:
            pos += 1
    return tokens_encontrados

# Código da função fornecida
codigo = """
def fun ( int x , str pal ) :
int y
y = x + conv ( pal )
return y
"""

# Analisando o código
tokens_encontrados = analisador_lexico(codigo)
print(tokens_encontrados)