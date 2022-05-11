import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

df = pd.read_csv("iris.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7,
                                         random_state=274946)

train_inputs = train_set[:, 0:-1]
train_classes = train_set[:, -1]
test_inputs = test_set[:, 0:-1]
test_classes = test_set[:, -1]

le = preprocessing.LabelEncoder()
# encode classes into numbers
train_classes_encoded=le.fit_transform(train_classes)
test_classes_encoded=le.fit_transform(test_classes)