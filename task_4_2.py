import os

import re
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True, description='Sample Commandline')

    parser.add_argument(
        '--file',
        action="store",
        help="path of file to take as input",
        nargs="?",
        metavar="file")

    args = parser.parse_args()

    print(args.file)
    file_input = args.file
    file_out = open("task_4_2_result.txt", "a")

    alphas = []
    rulesDict = {}
    with open(file_input, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
        rules = line[4:].replace(" ", "").split('|')
        alphas.append(line[0])
        rulesDict[line[0]] = rules
    #        print(alphas)
    #        print(rulesDict)

    def getCommonPref(rules):
        commonPref = []
        for rule in rules:
            i = rules.index(rule) + 1
            commonPerRule = []
            #print("rule", rule)
            while i < len(rules):
                retpre = os.path.commonprefix([rule, rules[i]])
                if retpre != "":
                    commonPerRule.append(retpre)
                    #print("commonPerRule", commonPerRule)
                i += 1
            if len(commonPerRule) > 0:
                commonPref.append(min(commonPerRule, key=len))
        if len(commonPref) > 0:
            #print("commonPref", min(commonPref, key=len))
            return min(commonPref, key=len)
        else:
            return "NO seq"

    def factor(commonPrefix, key):
        global rulesDict
        global alphas
        newAlpha = key + "'"
        alphas.append(newAlpha)
        alphaeli = []
        beta = []
        tobeAdded = "" + commonPrefix + "" + newAlpha
        beta.append(tobeAdded)
        for rule in rulesDict[key]:
            if rule[0] == commonPrefix:
                alphaeli.append(rule[1:])
            else:
                beta.append(rule)
        rulesDict[key] = beta
        rulesDict[newAlpha] = alphaeli

    def lefFac():
        dictStart = 0
        while dictStart < len(alphas):
            arryRules = rulesDict[alphas[dictStart]]
            commonPrefix = getCommonPref(arryRules)
            while commonPrefix != "NO seq":
                factor(commonPrefix, alphas[dictStart])
                commonPrefix = getCommonPref(rulesDict[alphas[dictStart]])
            dictStart += 1
            #print(rulesDict)

            #print(rulesDict)

    def filePrint():
        strRule = ""
        for key, val in rulesDict.items():
            strRule = key + " : "
            k = 0
            for rule in val:
                if rule != 'epsilon':
                    i = 0
                    while i < len(rule):
                        if len(rule) - i > 1:

                            if rule[i + 1] == "'":
                                #print(rule[i:])
                                strRule = strRule + rule[i:]
                                i = len(rule)
                            else:
                                strRule = strRule + "" + rule[i]
                                i += 1
                        else:
                            strRule = strRule + "" + rule[i]
                            i += 1

                        strRule = strRule + " "
                else:
                    strRule = strRule + "" + rule
                if len(val) - k > 1:
                    strRule = strRule + "| "
                k += 1

            #print(strRule)
            file_out.write(strRule)
            file_out.write("\n")
            strRule = ""

    lefFac()
    filePrint()
