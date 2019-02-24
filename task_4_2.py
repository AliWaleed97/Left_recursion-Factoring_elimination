import argparse
import numpy as np
import os
from collections import defaultdict

def readGrammar(path):
    grammar = dict()
    file = open(path, 'r')
    file = file.read().splitlines()
    for i in range(0,len(file)):
        file[i] = file[i].split(' : ')
        grammar[file[i][0]] = [f.replace(" ","") for f in file[i][1].split(' | ')]
    return grammar
def checkPrefix(value):
    prefix = defaultdict(list)
    for idx,v in enumerate(value):
        char = v[0]
        subArray = value[idx+1:]
        for element in subArray:
            if(element.startswith(char)):
                if(v not in prefix[char]):
                    prefix[char] += [v]
                prefix[char] += [element]
    return prefix

def leftFactoring2(grammar):
    # grammar = readGrammar(path)
    for key,value in grammar.items():
        prefix = checkPrefix(value)
        for k,v in prefix.items():
            grammar[key] = set(grammar[key]) - set(prefix[k])
            grammar[key] = list(grammar[key])
            grammar[key] += [k+''+k+"'"]
            grammar[k+"'"] = [x[1:] for x in set(v)]
            recursionCheck = checkPrefix(grammar[k+"'"])
            if(len(recursionCheck) > 0):
                leftFactoring2(grammar)
            # print(grammar[key])
            # leftFactoring2(grammar)
            printOutput(grammar)
            
            





            











# def leftFactoring(path):
#     grammar = readGrammar(path)
#     # print(grammar)
#     for key,value in grammar.items():
#         newGrammar = []
#         # print(key)
#         for v in value:
#             if(v.startswith(key)):
#                 # print(v)
#                 newGrammar.append(v)
#         value = set(value) - set(newGrammar)
#         grammar[key] = list(value)
#         grammar[key].append(key +''+ key+'^')
#         grammar[key+'^'] = [g[1:] for g in newGrammar]
#     printOutput(grammar)

def printOutput(grammar):
    output = open('task_4_2_result.txt', 'w')
    string = ""
    for key, values in grammar.items():
        output.write(key+' : ')
        for v in values:
            string+= v+' | '
        output.write(string[:-2])
        output.write('\n')
        string = ""
    print(grammar)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",metavar="file")
    args = parser.parse_args()
    grammar = readGrammar(args.file)
    leftFactoring2(grammar)
