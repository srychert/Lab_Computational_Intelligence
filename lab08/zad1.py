import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import numpy as np

df = pd.read_csv("iris.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7,
                                         random_state=274946)

train_inputs = train_set[:, 0:-1]
train_classes = train_set[:, -1]
test_inputs = test_set[:, 0:-1]
test_classes = test_set[:, -1]

def calc(cf):
    total = 0
    good = 0
    bad = 0
    for i, x in  np.ndenumerate(cf):
        if i[0] == i[1]:
            good += x
        else:
            bad += x
        total += x

    p = good/total
    return (round(p*100, 2))

for i in [3, 5, 11, 13]:
    knn = KNeighborsClassifier(n_neighbors=i, metric='euclidean')
    knn.fit(train_inputs, train_classes)

    y_pred = knn.predict(test_inputs)

    cf = confusion_matrix(test_classes, y_pred)
    p = calc(cf)
    print("{p}% for k={i}".format(p=p, i=i))
