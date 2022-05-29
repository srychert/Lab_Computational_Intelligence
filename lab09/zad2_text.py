import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')
nltk.download('wordnet')


def read_article(path):
    text = ''
    with open(path, "r") as file:
        text = file.read()
    return text


article1 = read_article("article.txt")
article2 = read_article("article2.txt")
article3 = read_article("article3.txt")

article1_tokenized = word_tokenize(article1)
article2_tokenized = word_tokenize(article2)
article3_tokenized = word_tokenize(article3)


def filter_words(words, stop_words):
    filtered_words = []
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)
    # word.isalnum() - alphanumeric
    # word.isalpha() - only alphabet characters
    return [word for word in filtered_words if word.isalpha()]


stop_words = set(stopwords.words("english"))

article1_filtered = filter_words(article1_tokenized, stop_words)
article2_filtered = filter_words(article2_tokenized, stop_words)
article3_filtered = filter_words(article3_tokenized, stop_words)
print(article1_filtered)


def stem_words(filtered_words):
    stemmer = SnowballStemmer("english")
    stemmed = []
    for word in filtered_words:
        stemmed.append(stemmer.stem(word))
    return stemmed


def lemmatize_words(filtered_words):
    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for word in filtered_words:
        lemmatized.append(lemmatizer.lemmatize(word))
    return lemmatized


# article1_stemmed = stem_words(article1_filtered)
# article2_stemmed = stem_words(article2_filtered)
# article3_stemmed = stem_words(article3_filtered)

article1_lemmatized = lemmatize_words(article1_filtered)
article2_lemmatized = lemmatize_words(article2_filtered)
article3_lemmatized = lemmatize_words(article3_filtered)

# docs = [' '.join(x) for x in [article1_stemmed , article2_stemmed, article3_stemmed]]
docs = [' '.join(x) for x in [article1_lemmatized, article2_lemmatized, article3_lemmatized]]
vec = CountVectorizer()
X = vec.fit_transform(docs)
df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names_out())
df.index = ['article1', 'article2', 'article3']
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df)
print(df)

with open('DTM.md', 'w') as f:
    f.write(df.to_markdown())