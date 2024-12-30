import re
from re import *

line = "bananas, 1 laranjas, 2 maçãs, 3 uvas, 4melancias, 555cerejas, 6 kiwis, etc."

res = re.split(r",", line, maxsplit= 0)

print(res)
print(len(res))