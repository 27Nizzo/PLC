from re import *

line1 = "hello world"
line2 = "goodbye world"
line3 = "HeLlO my boy!!"

res1 = match(r'(?i:hello)',line1)
print(res1)

res2 = match(r'(?i:hello)', line2)
print(res2)

res3 = match(r'(?i:hello)', line3)
print(res3)

