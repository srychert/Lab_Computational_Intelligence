import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import export_text
import json

df = pd.read_csv("diabetes.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7,
                                         random_state=274946)

# print(train_set)
# print(test_set)

train_inputs = train_set[:, 0:-1]
train_classes = train_set[:, -1]
test_inputs = test_set[:, 0:-1]
test_classes = test_set[:, -1]

X, y = train_inputs, train_classes
decision_tree = tree.DecisionTreeClassifier()
decision_tree = decision_tree.fit(X, y)

headers = list(df)
print(headers)

r = export_text(decision_tree, feature_names=headers[:-1])
print(r)

predictions = decision_tree.predict(test_inputs)

confusion_matrix = {}
for n in test_classes:
    confusion_matrix[n] = {"correct": 0, "wrong": 0}

good_predictions = 0
for i in range(len(predictions)):
    if predictions[i] == test_classes[i]:
        good_predictions = good_predictions + 1
        confusion_matrix[predictions[i]]["correct"] += 1
    else:
        confusion_matrix[predictions[i]]["wrong"] += 1

print(good_predictions)  # 164
print(good_predictions / len(predictions) * 100, "%")  # 71 %
print(json.dumps(confusion_matrix, sort_keys=False, indent=4))
