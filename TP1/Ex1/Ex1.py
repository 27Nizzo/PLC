import re

file = open("miniprocessos.txt","r")
lines = file.readlines()

## opcional

def TextCleanup():
    #clean = open("processosTrimmed.txt","w")

    for pr in lines:
        process = re.search("([0-9]+)[:]{2}.+",pr)
        if process != None:
            print(process)
            print(process.group(1))

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
    print(years)

## alínea b)
def NameFrequency():
    centuries = {}
    fn = "FirstName"
    ln = "LastName"

    for pr in lines:
        data = re.search('([0-9]+)[:]{2}([0-9]{4}\-[0-9]{2}\-[0-9]{2})[:]{2}',pr)
        names = re.findall('([a-z|A-Z| ]+[:])',pr)

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

                if listNames[0] not in centuries[century][fn]:
                    centuries[century][fn][listNames[0]] = 1
                else:
                    centuries[century][fn][listNames[0]] += 1

                if listNames[len(listNames)-2] not in centuries[century][ln]:
                    centuries[century][ln][listNames[len(listNames)-2]] = 1
                else:
                    centuries[century][ln][listNames[len(listNames)-2]] += 1

    for century in centuries:
        print("Século " + str(century) + ":")
        print(centuries[century], end = "\n\n")

## alínea c) 
def RecommendedFrequency():
    recommended = {}

    for pr in lines:
        data = re.findall('([A-Z][a-zA-Z ]+),([a-zA-Z ]+)\. ?(?i:(Proc\.[0-9]+))',pr)
        if data != None:
            familiar = []
            if data != []:
                print(data)
            for d in data:
                referente = d[1]
                if referente not in recommended:
                    familiar.append(referente)
                    recommended[referente] = 1
                elif referente not in familiar:
                    familiar.append(referente)
                    recommended[referente] += 1
    
    for familiar in recommended:
        print(familiar, end = " - ")
        print(recommended[familiar])

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

    for pai in progenitores:
        if len(progenitores[pai]) > 1:
            print(pai)

TextCleanup()

#YearlyFrequency()

#NameFrequency()

#RecommendedFrequency()

#MoreThanOneChildFrequency()