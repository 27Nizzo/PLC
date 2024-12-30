import re

pattern = r'^[A-Za-z]+(\.[A-Za-z]+|\.\?)*@\d{4}-\d{3};  \d{1,2},\d{2};-?\d{1,2},\d{2}$'

lines = [
    "RangelHenriques.Pedro@4715-012;41,55;-8,45",
    "Silva.Ana.Maria@4715-012;41,55;-9,00",
    "Araujo.?@4715-767;42,05;-9,55",
    "Mota.Carmo@4780-767;40,05;-8,55"
]

for line in lines:
    if re.match(pattern, line):
        print(f"Match: {line}")
    else:
        print(f"No match: {line}")