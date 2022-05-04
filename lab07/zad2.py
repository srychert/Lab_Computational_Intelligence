import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("iris.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7,
random_state=274946)

test_inputs = test_set[:, 0:4]

def classify_iris(sl, sw, pl, pw):
    if pw < 1:
        return("setosa")
    elif pw >= 1 and pw < 1.75:
        return("versicolor")
    else:
        return("virginica")

good_predictions = 0
len = test_set.shape[0]
for i in range(len):
    if classify_iris(*test_inputs[i]) == test_set[i][4]:
        good_predictions = good_predictions + 1


print(good_predictions) # 11
print(good_predictions/len*100, "%") # 24.4 %

# print(train_set)

# sort set by type
train_set = train_set[train_set[:,4].argsort()]

print(train_set)
