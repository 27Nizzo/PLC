import re
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

    return years

## alínea b)
def NameFrequency():
    centuries = {}
    fn = "FirstName"
    ln = "LastName"

    for pr in lines:
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})[:]{2}',pr)
        names = re.findall('([a-z|A-Z| ]+[:]{2})',pr)

        if data != None and names != None:
            date = data.group(2)
            date_components = re.split(r'-', date)
            year = date_components[0]
            century = int(int(year)/100)

            if century not in centuries:
                centuries[century] = {}
                centuries[century][fn] = {}
                centuries[century][ln] = {}

            for name in names:
                listNames = re.split('[ |:]',name)

                if listNames[0] != "":
                    if listNames[0] not in centuries[century][fn]:
                        centuries[century][fn][listNames[0]] = 1
                    else:
                        centuries[century][fn][listNames[0]] += 1

                    if listNames[len(listNames)-2] not in centuries[century][ln]:
                        centuries[century][ln][listNames[len(listNames)-2]] = 1
                    else:
                        centuries[century][ln][listNames[len(listNames)-2]] += 1

    return centuries

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
    
    return recommended

## alinea d)

def MoreThanOneChildFrequency():

    progenitores = {}

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

    return progenitores

TextCleanup()

YearlyFrequency()

NameFrequency()

RecommendedFrequency()

MoreThanOneChildFrequency()

# alinea e)

import json

def PrintToJson():
    processo = re.search("([0-9]+)[:]{2}([0-9]{4}-[0-9]{2}-[0-9]{2})[:]{2}(.+)",lines[1])
    componentesSemData = re.split("::",processo.group(3))
    componentesSemData.pop()
    processo_json = {
        "Numero" : processo.group(1),
        "Data" : processo.group(2),
        "Confessado" : componentesSemData[0],
        "Pai" : componentesSemData[1],
        "Mae" : componentesSemData[2],
        "Observacoes" : componentesSemData[3]
    }

    json_object = json.dumps(processo_json, indent=4)

    with open("PrimeiroRegisto.json", "w") as outfile:
        outfile.write(json_object)


PrintToJson()