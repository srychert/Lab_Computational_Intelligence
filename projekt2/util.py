import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
nltk.download('wordnet')



def filter_words(words, stop_words):
    filtered_words = []
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)
    # word.isalnum() - alphanumeric
    # word.isalpha() - only alphabet characters
    return [word for word in filtered_words if word.isalpha()]


stop_words = set(stopwords.words("english"))


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


# docs = [' '.join(x) for x in []]
# vec = CountVectorizer()
# X = vec.fit_transform(docs)
# df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names_out())
# df.index = ['article1', 'article2', 'article3']
# # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
# #     print(df)
# print("DTM:")
# print(df)
#
# with open('DTM.md', 'w') as f:
#     f.write(df.to_markdown())
#
# df_sum = df.sum(axis=1)
# tfdf = df.copy()
#
# for index, row in tfdf.iterrows():
#     tfdf.loc[index] = [x / df_sum[index] for x in row]
#
# print("TFDF:")
# print(tfdf)
#
# with open('TF.md', 'w') as f:
#     f.write(tfdf.to_markdown())
#
# tfvec = TfidfVectorizer()
# tdf = tfvec.fit_transform(docs)
# bow = pd.DataFrame(tdf.toarray(), columns=tfvec.get_feature_names_out())
# bow.index = ['article1', 'article2', 'article3']
#
# print("TFIDF:")
# print(bow)
#
# with open('TFIDF.md', 'w') as f:
#     f.write(bow.to_markdown())
#
# cosine_sim_matrix = cosine_similarity([tfdf.iloc[0], tfdf.iloc[1], tfdf.iloc[2]])
