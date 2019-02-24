import argparse
from collections import defaultdict

def readGrammar(path):
    grammar = dict()
    non_terminals = []
    file = open(path, 'r')
    file = file.read().splitlines()
    for i in range(0,len(file)):
        file[i] = file[i].split(' : ')
        non_terminals.append(file[i][0])
        grammar[file[i][0]] = [f.replace(" ","") for f in file[i][1].split(' | ')]
    return grammar,non_terminals

def printOutput(grammar):
    output = open('task_4_1_result.txt', 'w')
    string = ""
    for key, values in grammar.items():
        output.write(key+' : ')
        for v in values:
            string+= v+' | '
        output.write(string[:-2])
        output.write('\n')
        string = ""

def leftRecursionElimination(grammar,non_terminals):
    for i in range(0,len(non_terminals)):
        for j in range(0,i):
            i_grammar = grammar[non_terminals[i]]
            for g in i_grammar:
                if(g.startswith(non_terminals[j])):
                    grammar[non_terminals[i]].remove(g)
                    for rule in grammar[non_terminals[j]]:
                        grammar[non_terminals[i]] += [rule+''+g[1:]]

        rule = eliminateImmediateRecursion(non_terminals[i],grammar[non_terminals[i]])
        print(type(rule))
        if isinstance(rule,dict):
            print('dict')
            grammar[non_terminals[i]] = rule[non_terminals[i]]
            grammar[non_terminals[i]+"'"] = rule[non_terminals[i]+"'"]
    printOutput(grammar)


def eliminateImmediateRecursion(key,rule):
    grammar = rule
    alphas = []
    betas = []
    for g in grammar:
        if(g.startswith(key)):
            alphas.append(g[1:])
        else:
            betas.append(g)

    if(len(alphas) == 0):
        return rule
    else:
        rule = defaultdict(list)
        # rule_prime = []
        for beta in betas:
            rule[key] += [beta+''+key+"'"]
        for alpha in alphas:
            rule[key+"'"] += [alpha+''+key+"'"]
        rule[key+"'"] += ['epsilon']
    return rule

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",metavar="file")
    args = parser.parse_args()
    grammar,non_terminals = readGrammar(args.file)
    leftRecursionElimination(grammar,non_terminals)