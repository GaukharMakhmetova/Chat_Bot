from prettyTable import print_pretty_table
import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np


def checkFloat (n):
    return type(n) is float or (type(n).__module__ == np.__name__ and (n.dtype.type in [np.float16, np.float32, np.float64]))

def printAnswers(dataframe, answers):
    if dataframe.shape[0] == 1:
        text = "Exact match found"
    else:
        text = f'{dataframe.shape[0]} items found'
    print("\n{:-^80}\n".format(text))

    for index in dataframe.index:
        itemDesc = [["Property", "Value", "You asked"]]
        printDiff = False
        row = dataframe.loc[index]
        for i in dataframe:
            if pd.notnull(row[i]):
                diff = fuzz.partial_ratio(str(row[i]), answers[i]) < 90 and answers[i] != ""
                printDiff |= diff
                itemDesc.append(list(map(
                    lambda x: (str(x) if not checkFloat(x) else f'{x:.2f}').replace("\n", ""),
                    [i, row[i], answers[i] if diff else ""]
                )))

        if not printDiff:
            itemDesc = list(zip(*itemDesc))
            itemDesc.pop()
            itemDesc = list(zip(*itemDesc))

        print_pretty_table(itemDesc)
        print("\n")