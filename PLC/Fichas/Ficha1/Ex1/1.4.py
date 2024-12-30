import re 
from re import *

line = "Hello today I'm gonna talk about, hello, Hello and more. So just say HeLLo to start."

res = re.sub(r'(?i:hello)', "*YEP*", line, count = 0)

print(res)

line2 = "O meu telemóvel é 954324028 ou 9684122875 ou 931212411. O dele é 203604468. O do zé é 150305152"

res2 = re.sub(r"[0-2]", "p", line2)

res3 = re.sub(r"(2[1-9][0-9]{7}) | (9[1236][0-9]{7})", "++", line2)

print(res2)

print(res3)