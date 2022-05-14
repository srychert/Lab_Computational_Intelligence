import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

df = pd.read_csv("iris.csv")

(train_set, test_set) = train_test_split(df.values, train_size=0.7,
                                         random_state=274946)

train_inputs = train_set[:, 0:-1]
train_classes = train_set[:, -1]
test_inputs = test_set[:, 0:-1]
test_classes = test_set[:, -1]

le = preprocessing.LabelEncoder()
# encode classes into numbers
train_classes_encoded = le.fit_transform(train_classes)
test_classes_encoded = le.fit_transform(test_classes)

# scale inputs
scaler = StandardScaler()
scaler.fit(train_inputs)

train_inputs = scaler.transform(train_inputs)
test_inputs = scaler.transform(test_inputs)

def results(units, layers):
    # creating an classifier from the model
    # Multi-layer Perceptron classifier with hidden layers = layers each with n units = units
    mlp = MLPClassifier(hidden_layer_sizes=(units, ) * layers, max_iter=10000, random_state=274946)
    # fit the training data to our model
    mlp.fit(train_inputs, train_classes_encoded)

    predictions_train = mlp.predict(train_inputs)
    print("Train accuracy", accuracy_score(predictions_train, train_classes_encoded))
    predictions_test = mlp.predict(test_inputs)
    print("Test accuracy", accuracy_score(predictions_test, test_classes_encoded))

    probability_train = mlp.predict_proba(train_inputs)
    probability_test = mlp.predict_proba(test_inputs)

    # multi_output_train = []
    # multi_output_test = []

    train_correct_predictions = 0
    for i in range (len(probability_train)):
        row = probability_train[i]
        maxIndex = np.argmax(row)
        # b = np.zeros_like(row)
        # b[np.where(row == np.max(row))] = 1
        # multi_output_train.append(b)

        if maxIndex == train_classes_encoded[i]:
            train_correct_predictions += 1

    print(train_correct_predictions / len(probability_train))

    test_correct_predictions = 0
    for i in range (len(probability_test)):
        row = probability_test[i]
        maxIndex = np.argmax(row)
        # b = np.zeros_like(row)
        # b[np.where(row == np.max(row))] = 1
        # multi_output_test.append(b)

        if maxIndex == test_classes_encoded[i]:
            test_correct_predictions += 1

    print(test_correct_predictions / len(probability_test))

    # multi_output_train = np.array(multi_output_train)
    # multi_output_test = np.array(multi_output_test)


print("One hidden layer with 2 units")
results(2, 1) # 97, 98

print("\nOne hidden layer with 3 units")
results(3, 1) # 98, 95

print("\nTwo hidden layer with 3 units")
results(3, 2) # 66, 56 ???


