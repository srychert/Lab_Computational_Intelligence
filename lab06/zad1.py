import pandas as pd
import numpy as np
from difflib import SequenceMatcher

missing_values = ["n/a", "na", "--", "-"]
df = pd.read_csv("iris_with_errors.csv", na_values = missing_values)

# a) check how many missing values
def checkMissing(df):
    missing = df.isnull().sum().sum()
    print("Number of NA values:", missing)
    return missing

checkMissing(df)

# replace values not in range (0, 15) with NA values
for col in df:
    for i, row in enumerate(df[col]):
        try:
            value = float(row)
            if value <=0 or value >= 15:
                df.loc[i, col] = np.nan
        except ValueError:
            pass

checkMissing(df)

# Replace missing values with median of col
for col in df:
    try:
        median = df[col].median()
        df[col].fillna(median, inplace=True)
    except:
        pass


def checkSimilarity(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio()

types = ["Setosa", "Versicolor", "Virginica"]
for i, type in enumerate(df["variety"]):
    updated = False

    if type not in types:
        for defined_type in types:
            if checkSimilarity(defined_type.lower(), type.lower()) > 0.7:
                print('Should be: %-10s Is: %s' % (defined_type, type))
                df.at[i,'variety'] = defined_type
                updated = True

        # drop rows that can't be fixed
        if not updated:
            df = df.drop(labels=i, axis=0)

print("\nData frame shape after cleanup:", df.shape)
print("\nIndex", df.head())
