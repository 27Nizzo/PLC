import re 


def parseS():
    if lookahead == r'a(?=b)':
        eat('a')
        parseS()
        eat('b')
    elif lookahead == r'$':
        eat('end')
    else:
        error()