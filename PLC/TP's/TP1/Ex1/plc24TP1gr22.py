import re
import json
## opcional

def TextCleanup():
    file = open("processos.txt","r")
    lines = file.readlines()
    clean = open("processosTrimmed.txt","w")
    clean.write("NumProc::Data::Confessado::Pai::Mae::Observacoes::\n")
    processos = {}
    processosRealocar = []
    maxProcessNumber = 0

    for pr in lines:
        process = re.search("([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})[:]{2}(.+)",pr)
        if process != None:
            processNumber = process.group(1)
            processData = re.split(r'-',process.group(2))
            processPeople = re.split(r'::',process.group(3))
            processPeople.pop()

            if int(processNumber) > maxProcessNumber:
                maxProcessNumber = int(processNumber)

            if processNumber not in processos:
                processos[processNumber] = {}
                processos[processNumber]["string"] = pr
                processos[processNumber]["ano"] = processData[0]
                processos[processNumber]["mes"] = processData[1]
                processos[processNumber]["dia"] = processData[2]
                processos[processNumber]["pessoas"] = processPeople
            
            elif processos[processNumber]["ano"] > processData[0]:
                processosRealocar.append(processos[processNumber]["string"])
                processos[processNumber]["string"] = pr
                processos[processNumber]["ano"] = processData[0]
                processos[processNumber]["mes"] = processData[1]
                processos[processNumber]["dia"] = processData[2]
                processos[processNumber]["pessoas"] = processPeople
            
            elif processos[processNumber]["mes"] > processData[1]:
                processosRealocar.append(processos[processNumber]["string"])
                processos[processNumber]["string"] = pr
                processos[processNumber]["ano"] = processData[0]
                processos[processNumber]["mes"] = processData[1]
                processos[processNumber]["dia"] = processData[2]
                processos[processNumber]["pessoas"] = processPeople

            elif processos[processNumber]["dia"] > processData[2]:
                processosRealocar.append(processos[processNumber]["string"])
                processos[processNumber]["string"] = pr
                processos[processNumber]["ano"] = processData[0]
                processos[processNumber]["mes"] = processData[1]
                processos[processNumber]["dia"] = processData[2]
                processos[processNumber]["pessoas"] = processPeople
            elif processos[processNumber]["pessoas"][0] != processPeople[0] and processos[processNumber]["pessoas"][1] != processPeople[1] and processos[processNumber]["pessoas"][2] != processPeople[2]:
                processosRealocar.append(pr)

    for pr in processos:
        processo = pr + "::" + processos[pr]["ano"] + "-" + processos[pr]["mes"] + "-" + processos[pr]["dia"] + "::"
        for person in processos[pr]["pessoas"]:
            processo = processo + person + "::"
        processo = processo + "\n"
        clean.write(processo)
    
    for pr in processosRealocar:
        process = re.search("([0-9]+)(.+)",pr)
        maxProcessNumber += 1
        newProcess = str(maxProcessNumber) + process.group(2) + "\n"
        clean.write(newProcess)

file = open("processosTrimmed.txt","r")
lines = file.readlines()

## alínea a) Calcular a frequência de Processos por ano (primeiro elemento da data)
def YearlyFrequency():
    # Inicializa um dicionário vazio para armazenar a contagem de processos por ano
    years = {}

    # Itera por cada linha no arquivo/processo listado
    for pr in lines:
        # Usa uma expressão regular para capturar o número do processo e a data (no formato AAAA-MM-DD)
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})', pr)

        # Se houver uma correspondência válida na linha
        if data != None:
            # Extrai a data da correspondência
            date = data.group(2)
            # Divide a data nos componentes [AAAA, MM, DD] usando '-' como delimitador
            date_components = re.split(r'-', date)
            # Seleciona o ano (primeiro elemento da lista)
            year = date_components[0]

            # Verifica se o ano já existe no dicionário 'years'
            if year not in years:
                # Se não, adiciona o ano com contagem inicial de 1
                years[year] = 1
            else:
                # Se já existir, incrementa a contagem para o ano
                years[year] += 1

    # Converte o dicionário 'years' para um objeto JSON com indentação para fácil visualização
    json_object = json.dumps(years, indent=4)

    # Retorna o objeto JSON com a contagem de processos por ano
    return json_object


## alínea b)
def NameFrequency():
    # Inicializa um dicionário vazio para armazenar contagens de nomes por século
    centuries = {}
    fn = "FirstName"  # Definição de chave para primeiros nomes
    ln = "LastName"   # Definição de chave para sobrenomes

    # Itera por cada linha nos processos
    for pr in lines:
        # Usa expressão regular para capturar o número do processo e a data no formato AAAA-MM-DD
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})', pr)
        # Usa outra expressão regular para capturar os nomes
        names = re.findall('[:]{2}([a-z|A-Z| ]+[:]{2})', pr)

        # Verifica se a data e os nomes foram encontrados
        if data != None and names != None:
            # Extrai o ano da data e calcula o século
            date = data.group(2)
            date_components = re.split(r'-', date)
            year = date_components[0]
            century = int(int(year) / 100)

            # Se o século ainda não existe no dicionário, inicializa as estruturas de dados
            if century not in centuries:
                centuries[century] = {}
                centuries[century][fn] = {}  # Dicionário para contagem de primeiros nomes
                centuries[century][ln] = {}  # Dicionário para contagem de sobrenomes
                centuries[century]["nomes"] = []  # Lista temporária para todos os nomes do século

            # Itera por cada nome na lista de nomes encontrados
            for name in names:
                # Se o nome não está na lista temporária e não começa com uma vírgula
                if name not in centuries[century]["nomes"] and name[0] != ",":
                    centuries[century]["nomes"].append(name)  # Adiciona o nome à lista
                    # Divide o nome em partes (nome e sobrenome) e remove o último elemento vazio
                    listNames = re.split('[ |:]', name)
                    listNames.pop()

                    # Adiciona o primeiro nome ao dicionário 'FirstName' com contagem
                    if listNames[0] != "":
                        if listNames[0] not in centuries[century][fn]:
                            centuries[century][fn][listNames[0]] = 1
                        else:
                            centuries[century][fn][listNames[0]] += 1

                        # Adiciona o último nome ao dicionário 'LastName' com contagem
                        if listNames[len(listNames) - 2] not in centuries[century][ln]:
                            centuries[century][ln][listNames[len(listNames) - 2]] = 1
                        else:
                            centuries[century][ln][listNames[len(listNames) - 2]] += 1

    # Remove a lista temporária de nomes ('nomes') de cada entrada de século no dicionário
    for c in centuries:
        centuries[c].pop("nomes")

    # Converte o dicionário 'centuries' para um objeto JSON com indentação
    json_object = json.dumps(centuries, indent=4)

    # Retorna o objeto JSON com as contagens de primeiros e últimos nomes por século
    return json_object


## alínea c) 
def RecommendedFrequency():
    # Inicializa um dicionário para armazenar a frequência de recomendação
    recommended = {}

    # Itera por cada linha nos processos
    for pr in lines:
        # Usa expressão regular para capturar informações de recomendação na linha:
        # Primeiro Nome, Nome de Referência e Número de Processo
        data = re.findall('([A-Z][a-zA-Z ]+),([a-zA-Z ]+)\. ?(?i:(Proc\.[0-9]+))', pr)
        
        # Verifica se há dados correspondentes encontrados na linha
        if data != None:
            familiar = []  # Lista temporária para armazenar referências familiares

            # Itera por cada conjunto de dados capturados na linha
            for d in data:
                referente = d[1]  # Nome de referência extraído do grupo de dados

                # Se o nome de referência ainda não está no dicionário, inicializa com valor 1
                if referente not in recommended:
                    familiar.append(referente)
                    recommended[referente] = 1

                # Se o nome de referência já está no dicionário, mas não foi contado nesta linha, incrementa
                elif referente not in familiar:
                    familiar.append(referente)
                    recommended[referente] += 1

    # Converte o dicionário 'recommended' em um objeto JSON com indentação
    json_object = json.dumps(recommended, indent=4)

    # Retorna o objeto JSON com as frequências de recomendação
    return json_object


## alinea d) Identificar todos os Pais que tenham mais do que 1 Filho Confessado;

def MoreThanOneChildFrequency():
    # Inicializa um dicionário para armazenar os progenitores e seus filhos
    progenitores = {}
    morethan = {}  # Dicionário para armazenar progenitores com mais de um filho

    # Itera por cada linha no conjunto de dados 'lines'
    for pr in lines:
        # Captura a data do processo e os nomes de confessado, pai e mãe na linha
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})[:]{2}', pr)
        names = re.search('([a-z|A-Z| ]+)[:]{2}([a-z|A-Z| ]+)[:]{2}([a-z|A-Z| ]+)[:]{2}', pr)
        
        # Verifica se foram encontrados dados válidos
        if data != None and names != None:
            confessado = names.group(1)  # Nome do confessado (filho)
            pai = names.group(2)  # Nome do pai
            mae = names.group(3)  # Nome da mãe

            # Adiciona o pai ao dicionário, se ainda não estiver presente
            if pai not in progenitores:
                progenitores[pai] = []
            
            # Adiciona o confessado à lista de filhos do pai, se ainda não estiver na lista
            if confessado not in progenitores[pai]:
                progenitores[pai].append(confessado)
            
            # Adiciona a mãe ao dicionário, se ainda não estiver presente
            if mae not in progenitores:
                progenitores[mae] = []
            
            # Adiciona o confessado à lista de filhos da mãe, se ainda não estiver na lista
            if confessado not in progenitores[mae]:
                progenitores[mae].append(confessado)

    # Filtra progenitores com mais de um filho e adiciona ao dicionário 'morethan'
    for pai in progenitores:
        if len(progenitores[pai]) > 1:
            morethan[pai] = progenitores[pai]

    # Converte o dicionário 'morethan' em um objeto JSON com indentação
    json_object = json.dumps(morethan, indent=4)

    # Retorna o objeto JSON com os progenitores que têm mais de um filho
    return json_object


# alinea e)

def PrintToJson():
    # Extrai informações de um registro de processo específico (neste caso, a segunda linha do conjunto de dados 'lines')
    processo = re.search("([0-9]+)[:]{2}([0-9]{4}-[0-9]{2}-[0-9]{2})[:]{2}(.+)", lines[1])

    # Separa as informações do registro removendo a data e usando '::' como delimitador
    componentesSemData = re.split("::", processo.group(3))
    componentesSemData.pop()  # Remove o último elemento vazio, gerado pelo delimitador '::' final

    # Cria um dicionário JSON com as informações do processo:
    # - Número do processo, data, confessado, pai, mãe e observações
    processo_json = {
        "Processo " + processo.group(1): {  # Nome do processo, ex: "Processo 123"
            "Data": processo.group(2),  # Data do processo
            "Confessado": componentesSemData[0],  # Nome do confessado
            "Pai": componentesSemData[1],  # Nome do pai
            "Mae": componentesSemData[2],  # Nome da mãe
            "Observacoes": componentesSemData[3]  # Observações adicionais
        },
    }

    # Converte o dicionário do processo para um objeto JSON, formatado com indentação
    json_object = json.dumps(processo_json, indent=4)

    # Escreve o JSON resultante num ficheiro chamado "PrimeiroRegisto.json"
    with open("PrimeiroRegisto.json", "w") as outfile:
        outfile.write(json_object)


# Executa a função para criar o ficheiro JSON com o primeiro registro de processo
PrintToJson()


if __name__ == "__main__":
    html = "".join(["""<!DOCTYPE html>
        <html>
        <body>

        <h1>PLC TP1 - Grupo 22</h1>
        <h2>1 - Processador de Pessoas Listadas nos Róis de Confessados</h2>

        <select onchange="change_select(this.value)">
            <option value="">Choose an option:</option>
            <option value="YearlyFrequency">Frequência de processos por ano</option>
            <option value="NameFrequency">Frequência de nomes</option>
            <option value="RecommendedFrequency">Confessados Recomendados</option>
            <option value="MoreThanOneChildFrequency">Pais com mais de um Filho Confessado</option>
        </select>

        <p id="table1"></p>
        <p id="table2"></p>
        <p id="table3"></p>

        <script>
            const results = {""" 
    , f""" "YearlyFrequency" : {YearlyFrequency()}, 
            "NameFrequency" : {NameFrequency()},
            "RecommendedFrequency" : {RecommendedFrequency()},
            "MoreThanOneChildFrequency" : {MoreThanOneChildFrequency()}  """
    , r"""} 
            function change_select(select) {
                const choice = results[select];
                console.log(choice);
                let text = "";
                const fn = "FirstName"; 
                const ln = "LastName";
                    if (select == "MoreThanOneChildFrequency"){
                        document.getElementById("table2").innerHTML = "";
                        document.getElementById("table3").innerHTML = "";
                        const l = Object.keys(choice).length;
                        text += <select onchange="choose_parent(this.value)" >
                        text += <option value="">Choose an option:</option>
                            for (let y in choice){
                                text += <option value="${choice[y]}"> ${y} </option> 
                            }
                        text += "</select>";
                        text +=  ---  Número de Pais com mais de um Filho Confessado : ${l}
                    }

                    else {
                        if (select == "YearlyFrequency"){
                            document.getElementById("table2").innerHTML = "";
                            document.getElementById("table3").innerHTML = "";
                            text += Ano <select onchange="choose_year(this.value)" >
                            text += <option value="0">Choose an option:</option>
                            for (let y in choice){
                                text += <option value="${choice[y]}"> ${y} </option>
                            }
                            text += </select> ;
                        }
                        else {
                            if (select == "NameFrequency"){
                            document.getElementById("table2").innerHTML = "";
                            document.getElementById("table3").innerHTML = "";
                            text += Século <select onchange="choose_FLname(this.value)" >
                            text += <option value="">Choose an option:</option>
                            for (let y in choice){
                                console.log(choice[y])
                                text += <option value=${JSON.stringify(choice[y])}> ${y}</option>
                            }
                            text += </select> ;
                            }
                            
                            else {
                                if (select == "RecommendedFrequency"){
                                    document.getElementById("table2").innerHTML = "";
                                    document.getElementById("table3").innerHTML = "";
                                    text += Recomendador <select onchange="choose_recomended(this.value)" >
                                    text += <option value="0">Choose an option:</option>
                                    for (let y in choice){
                                        text += <option value="${choice[y]}"> ${y} </option>
                                    }
                                    text += </select> ;
                                }
                            }
                        }
                    }
                document.getElementById("table1").innerHTML = text;
            }

            function choose_parent(select){
                const array = select.split(",");
                text = "Número de Filhos Confessados : " + array.length.toString() + "<br />" + "<br />";
                
                for (let f in array){
                    text += ${array[f]}, <br />
                }

                document.getElementById("table2").innerHTML = text;
            }

            function choose_year(select){
                document.getElementById("table2").innerHTML = Número de processos :: ${select};
            }

            function choose_recomended(select){
                document.getElementById("table2").innerHTML = Número de processos recomendados :: ${select};
            }

            function choose_FLname(select){
                const obj = JSON.parse(select);
                const fn = Object.keys(obj)[0];
                const ln = Object.keys(obj)[1];
                console.log(obj)
                let text = "";

                text = Nomes Próprios ou Apelidos: <select onchange="choose_name(this.value)" >;
                text += <option value="0">Choose an option:</option>;
                text += <option value=${JSON.stringify(obj[fn])}> Nomes Próprios </option>;
                text += <option value=${JSON.stringify(obj[ln])}> Apelidos </option>;
                text += </select> ;
                document.getElementById("table2").innerHTML = text;
            }

            function choose_name(select){
                const array = JSON.parse(select);
                text = "";
                
                for (let f in array){
                    text += ${f} :: ${array[f]}, <br />
                }

                document.getElementById("table3").innerHTML = text;
            }

        </script>

        </body>
        </html>"""
])
    with open("index.html", "w") as outfile:
        outfile.write(html)