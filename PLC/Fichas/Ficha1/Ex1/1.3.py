import re
from re import *

line1 = "Hello today we are going to say a BIG HELLO!"
line2 = "Hello, heLO, HelLo, HELLO, heLLo"
line3 = "NOTHING"

res1 = re.findall(r'(?i:hello)', line1)
print(res1)
print(len(res1))

res2 = re.findall(r'(?i:hello)', line2)
print(res2)
print(len(res2))

res3 = re.findall(r'(?i:hello)', line3)
print(res3)
print(len(res3))
