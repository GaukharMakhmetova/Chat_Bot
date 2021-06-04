from collections import defaultdict, Counter
import numpy as np
import re
from fuzzywuzzy import process, fuzz
from rules import rulesDict, rulesComments
from collections import Counter

def dialog(xl, productType):
    # import Levenshtein
    # keys = list(rulesDict.keys())
    # distnts = list(map(lambda x: Levenshtein.distance("MCCB", x), keys))
    # key = keys[distnts.index(min(distnts))]

    key = process.extractOne(productType, rulesDict.keys())[0]
    askList = rulesDict[key]
    comList = defaultdict(str, rulesComments[key])

    dataframe = xl.parse(productType)
    dataframe = dataframe.loc[:, ~dataframe.columns.str.contains('^Unnamed:')]
    # Soft strip()
    dataframe = dataframe.replace(r'^\s+|\s+$', '', regex=True)
    answers = defaultdict(str)

    for parametr in askList:

        characterValue = ""
        for columnName in dataframe:
            if fuzz.ratio(columnName.replace('\n', ""), parametr) > 90:
                tempDataSeries = dataframe[columnName].astype(np.str_)
                break

        if comList and comList[parametr]:
            print(comList[parametr])
        variants = np.unique(tempDataSeries)
        variantslen = len(variants)
        variants.sort()
        if variantslen == 1:
            characterValue = variants[0]
        else:
            print('-' * 80, f'\nEnter value for "{parametr}"')
            if variantslen <= 10:
                print('Variants:\n', "\n".join(list(map(lambda x, y: f'\t{x}: {y}', range(len(variants)), variants))))
                while not characterValue:
                    answerInp = input('Enter correct number: ')
                    answer = answerInp
                    if answer.isnumeric():
                        answer = int(answer)
                        if -1 < answer < variantslen:
                            characterValue = variants[answer]
            else:
                print('Examples:\n\t', ", ".join(variants[:10]))
                while not characterValue:
                    answerInp = input('Enter value: ')
                    answer = answerInp
                    if "rated current" in parametr.lower():
                        answer = float((re.sub(r"[^.0-9]", "", answer.replace(",", "."))))
                        floatVariants = list(map(lambda z: (float(re.sub(r"[^.0-9]", "", z)), z), variants))
                        floatVariants.sort(key=lambda x: x[0])
                        for sortedVarianValue in floatVariants:
                            if answer <= sortedVarianValue[0]:
                                characterValue = sortedVarianValue[1]
                                break
                        if not characterValue: print(f"Maximum: {max(floatVariants)[1]}")
                    else:
                        fastKey = lambda xxx: max(xxx, key=lambda x: x[1])[0]

                        selected1 = process.extractOne(answer.replace(" ", ""), variants)[0]

                        selected2 = fastKey(list(map(lambda x: (x, fuzz.ratio(answer, x)), variants)))

                        temp = list(
                            zip(*list(map(lambda z: list(map(lambda x: fuzz.ratio(z, x), variants)), answer.split()))))
                        selected3 = fastKey(list(map(lambda x, z: (z, sum(x)), temp, variants)))

                        temp = list(
                            zip(*list(map(lambda z: list(map(lambda x: fuzz.WRatio(z, x), variants)), answer.split()))))
                        selected4 = fastKey(list(map(lambda x, z: (z, sum(x)), temp, variants)))

                        if not (selected1 == selected2 == selected3 == selected4):
                            selected = [selected1, selected2, selected3, selected4]
                            c = Counter(selected)
                            for elem in c:
                                if c[elem] == 3:
                                    if (input(
                                            f'Do you mean: {elem}? (y - continue, other key - repeat)\n').lower() == 'y'):
                                        characterValue = elem
                            if not characterValue:
                                print("Сan't determine the appropriate value. Here's a similar one:\n\t", selected)
                                print("Please repeat")
                        else:
                            characterValue = selected1
                answers[columnName] = answerInp
        dataframe = dataframe[tempDataSeries == np.array(characterValue, tempDataSeries.dtype)]
        if dataframe.shape[0] == 1: break

    return dataframe, answers