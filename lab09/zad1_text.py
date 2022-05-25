import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

text = ''

with open("article.txt", "r") as file:
    text = file.read()

tokenized_word=word_tokenize(text)
print(tokenized_word)
print(len(tokenized_word))


stop_words=set(stopwords.words("english"))
print(stop_words)

filtered_word=[]
for w in tokenized_word:
    if w not in stop_words:
        filtered_word.append(w)

print("Filterd Sentence:",filtered_word)
print(len(filtered_word))


from nltk.stem.wordnet import WordNetLemmatizer
lem = WordNetLemmatizer()

from nltk.stem.porter import PorterStemmer
stem = PorterStemmer()

stemmead = []

for word in filtered_word:
    # lem.lemmatize(word, "v")
    stemmead.append(stem.stem(word))

# print("Lemmatized Word:",lem.lemmatize(filtered_word,"v"))
# print("Stemmed Word:",stem.stem(filtered_word))

print(len(stemmead))


# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.tokenize import RegexpTokenizer
#
# #tokenizer to remove unwanted elements from out data like symbols and numbers
# token = RegexpTokenizer(r'[a-zA-Z0-9]+')
# cv = CountVectorizer(lowercase=True,stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)
# text_counts= cv.fit_transform(data['Phrase'])

fd = nltk.FreqDist(stemmead)

print(fd)

fd.most_common(3)
fd.tabulate(3)

