import pandas as pd
from time import time
from selectItems import dialog
from printAnswers import printAnswers

file = "Electrical Products Price Sheet - 2019-2020.xlsx"

#TODO Adapt for a different number of header lines (2-3 lines)
#TODO Adapt to comments about the specification after the header (several lines to skip)
#TODO Remove duplicate columns
a = time()

xl = pd.ExcelFile(file)
names = xl.sheet_names

nextIteration = True

while nextIteration:
    print('-' * 80)
    print("\nSelect product type:\n", "\n".join(list(map(lambda x, y: f'\t{x}: {y}', range(len(names)), names))))
    page = ""
    while not page.isnumeric():
        page = input("\nEnter the number: ")
    productType = names[int(page)]
    print("Selected:", productType)

    dataframe, answers = dialog(xl, productType)
    printAnswers(dataframe, answers)

    print('-'*80)
    nextIteration = input("Press Enter if you want to pick up another item, or write something for stop\n") == ""


