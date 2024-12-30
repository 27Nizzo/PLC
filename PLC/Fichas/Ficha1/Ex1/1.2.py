import re
from re import *

line1 = "Hello, how are you?"
line2 = "Today I'm gonna say hello to the first person I see"
line3 = "Nothing"
line4 = "Just say HeLlo"
line5 = "HeLLo, Hello, HELLO, hello there! hello, girls!! hello, guys!!!"


res1 = re.search(r'(?i:hello)', line1)
print(res1)

res2 = re.search(r'(?i:hello)', line2)
print(res2)

res3 = re.search(r'(?i:hello)', line3)
print(res3)

res4 = re.search(r'(?i:hello)', line4)
print(res4)

res5 = re.search(r'(?i:hello)', line5)
print(res5)