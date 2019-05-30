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
    file_out = open("task_4_1_result.txt", "a")

    alphas = []
    rulesDict = {}
    with open(file_input, 'r') as f:
        lines = f.readlines()
        print(lines)
        for line in lines:
            line = line.strip()
            rules = line[4:].replace(" ", "").split('|')
            alphas.append(line[0])
            rulesDict[line[0]] = rules
        print(alphas)
        print(rulesDict)

    def eliminateDirect(alpha):
        global rulesDict
        strRuleNew = "" + alpha + "'"
        tobeelim = False
        alphaElim = []
        beta = []
        rulesArray = rulesDict[alpha]
        for rule in rulesArray:
            if rule[0] == alpha:
                tobeelim = True
                strAlpha = "" + rule[1:] + strRuleNew
                alphaElim.append(strAlpha)
            else:
                strBeta = "" + str(rule[0:]) + strRuleNew
                beta.append(strBeta)
        if tobeelim:
            rulesDict[alpha] = beta
            alphaElim.append("epsilon")
            rulesDict[strRuleNew] = alphaElim
        print(rulesDict)

    def ruleInAIHasAJasRule(i, j):
        rulesAI = rulesDict[alphas[i]]
        alphaAJ = alphas[j]
        for rule in rulesAI:
            if rule[0] == alphaAJ:
                return True
        return False

    def addRulesOfAJinAI(i, j):
        alphaAJ = alphas[j]
        rulesAJ = rulesDict[alphas[j]]
        rulesAI = rulesDict[alphas[i]]
        for rule in rulesAI:
            if rule[0] == alphaAJ:
                newRules = []
                for ruleAj in rulesAJ:
                    strRule = "" + ruleAj + "" + rule[1:]
                    newRules.append(strRule)
                rulesAI.remove(rule)
                rulesAI = rulesAI + newRules
        rulesDict[alphas[i]] = rulesAI

    def GeneralLeftRec():
        for alpha in alphas:
            j = 0
            i = alphas.index(alpha)
            while j < i:
                if ruleInAIHasAJasRule(i, j):
                    addRulesOfAJinAI(i, j)
                j += 1
            eliminateDirect(alpha)

    def filePrint():
        strRule = ""
        for key, val in rulesDict.items():
            strRule = key + " : "
            k = 0
            for rule in val:
                if rule != 'epsilon':
                    i = 0
                    while i < len(rule):
                        strRule = strRule + "" + rule[i]
                        if len(rule) - i > 1:
                            if rule[i + 1] == "'":
                                strRule = strRule + rule[i + 1]
                                i = i + 2
                            else:
                                i += 1
                        else:
                            i += 1
                        strRule = strRule + " "
                else:
                    strRule = strRule + "" + rule
                if len(val) - k > 1:
                    strRule = strRule + "| "
                k += 1

            print(strRule)
            file_out.write(strRule)
            file_out.write("\n")
            strRule = ""

    GeneralLeftRec()
    filePrint()