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

## alínea a)
def YearlyFrequency():
    years = {}

    for pr in lines:
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})',pr)

        if data != None:
            date = data.group(2)
            date_components = re.split(r'-', date)
            year = date_components[0]

            if year not in years:
                years[year] = 1
            else:
                years[year] += 1

    json_object = json.dumps(years, indent=4)

    return json_object

## alínea b)
def NameFrequency():
    centuries = {}
    fn = "FirstName"
    ln = "LastName"

    for pr in lines:
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})',pr)
        names = re.findall('[:]{2}([a-z|A-Z| ]+[:]{2})',pr)

        if data != None and names != None:
            date = data.group(2)
            date_components = re.split(r'-', date)
            year = date_components[0]
            century = int(int(year)/100)

            if century not in centuries:
                centuries[century] = {}
                centuries[century][fn] = {}
                centuries[century][ln] = {}
                centuries[century]["nomes"] = []

            for name in names:
                if name not in centuries[century]["nomes"] and name[0] != "," :
                    centuries[century]["nomes"].append(name)
                    listNames = re.split('[ |:]',name)
                    listNames.pop()

                    if listNames[0] != "":
                        if listNames[0] not in centuries[century][fn]:
                            centuries[century][fn][listNames[0]] = 1
                        else:
                            centuries[century][fn][listNames[0]] += 1

                        if listNames[len(listNames)-2] not in centuries[century][ln]:
                            centuries[century][ln][listNames[len(listNames)-2]] = 1
                        else:
                            centuries[century][ln][listNames[len(listNames)-2]] += 1

    for c in centuries:
        centuries[c].pop("nomes")

    json_object = json.dumps(centuries, indent=4)

    return json_object

## alínea c) 
def RecommendedFrequency():
    recommended = {}

    for pr in lines:
        data = re.findall('([A-Z][a-zA-Z ]+),([a-zA-Z ]+)\. ?(?i:(Proc\.[0-9]+))',pr)
        if data != None:
            familiar = []
            for d in data:
                referente = d[1]
                if referente not in recommended:
                    familiar.append(referente)
                    recommended[referente] = 1
                elif referente not in familiar:
                    familiar.append(referente)
                    recommended[referente] += 1
    
    json_object = json.dumps(recommended, indent=4)

    return json_object

## alinea d)

def MoreThanOneChildFrequency():

    progenitores = {}
    morethan = {}

    for pr in lines:
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})[:]{2}',pr)
        names = re.search('([a-z|A-Z| ]+)[:]{2}([a-z|A-Z| ]+)[:]{2}([a-z|A-Z| ]+)[:]{2}',pr)
        
        if data != None and names != None:
            confessado = names.group(1)
            pai = names.group(2)
            mae = names.group(3)

            if pai not in progenitores:
                progenitores[pai] = []
            
            if confessado not in progenitores[pai]:
                progenitores[pai].append(confessado)
            
            if mae not in progenitores:
                progenitores[mae] = []
            
            if confessado not in progenitores[mae]:
                progenitores[mae].append(confessado)

    for pai in progenitores:
        if len(progenitores[pai]) > 1:
            morethan[pai] = progenitores[pai]

    json_object = json.dumps(morethan, indent=4)

    return json_object

# alinea e)

def PrintToJson():
    processo = re.search("([0-9]+)[:]{2}([0-9]{4}-[0-9]{2}-[0-9]{2})[:]{2}(.+)",lines[1])
    componentesSemData = re.split("::",processo.group(3))
    componentesSemData.pop()
    processo_json = {
        "Processo " + processo.group(1) : {
            "Data" : processo.group(2),
            "Confessado" : componentesSemData[0],
            "Pai" : componentesSemData[1],
            "Mae" : componentesSemData[2],
            "Observacoes" : componentesSemData[3]
        },
    }

    json_object = json.dumps(processo_json, indent=4)

    with open("PrimeiroRegisto.json", "w") as outfile:
        outfile.write(json_object)


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
                        text += `<select onchange="choose_parent(this.value)" >`
                        text += `<option value="">Choose an option:</option>`
                            for (let y in choice){
                                text += `<option value="${choice[y]}"> ${y} </option>` 
                            }
                        text += "</select>";
                        text += ` ---  Número de Pais com mais de um Filho Confessado : ${l}`
                    }

                    else {
                        if (select == "YearlyFrequency"){
                            document.getElementById("table2").innerHTML = "";
                            document.getElementById("table3").innerHTML = "";
                            text += `Ano <select onchange="choose_year(this.value)" >`
                            text += `<option value="0">Choose an option:</option>`
                            for (let y in choice){
                                text += `<option value="${choice[y]}"> ${y} </option>`
                            }
                            text += `</select> `;
                        }
                        else {
                            if (select == "NameFrequency"){
                            document.getElementById("table2").innerHTML = "";
                            document.getElementById("table3").innerHTML = "";
                            text += `Século <select onchange="choose_FLname(this.value)" >`
                            text += `<option value="">Choose an option:</option>`
                            for (let y in choice){
                                console.log(choice[y])
                                text += `<option value=${JSON.stringify(choice[y])}> ${y}</option>`
                            }
                            text += `</select> `;
                            }
                            
                            else {
                                if (select == "RecommendedFrequency"){
                                    document.getElementById("table2").innerHTML = "";
                                    document.getElementById("table3").innerHTML = "";
                                    text += `Recomendador <select onchange="choose_recomended(this.value)" >`
                                    text += `<option value="0">Choose an option:</option>`
                                    for (let y in choice){
                                        text += `<option value="${choice[y]}"> ${y} </option>`
                                    }
                                    text += `</select> `;
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
                    text += `${array[f]}, <br />`
                }

                document.getElementById("table2").innerHTML = text;
            }

            function choose_year(select){
                document.getElementById("table2").innerHTML = `Número de processos :: ${select}`;
            }

            function choose_recomended(select){
                document.getElementById("table2").innerHTML = `Número de processos recomendados :: ${select}`;
            }

            function choose_FLname(select){
                const obj = JSON.parse(select);
                const fn = Object.keys(obj)[0];
                const ln = Object.keys(obj)[1];
                console.log(obj)
                let text = "";

                text = `Nomes Próprios ou Apelidos: <select onchange="choose_name(this.value)" >`;
                text += `<option value="0">Choose an option:</option>`;
                text += `<option value=${JSON.stringify(obj[fn])}> Nomes Próprios </option>`;
                text += `<option value=${JSON.stringify(obj[ln])}> Apelidos </option>`;
                text += `</select> `;
                document.getElementById("table2").innerHTML = text;
            }

            function choose_name(select){
                const array = JSON.parse(select);
                text = "";
                
                for (let f in array){
                    text += `${f} :: ${array[f]}, <br />`
                }

                document.getElementById("table3").innerHTML = text;
            }

        </script>

        </body>
        </html>"""
])
    with open("index.html", "w") as outfile:
        outfile.write(html)
