import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

text = ''

with open("article.txt", "r") as file:
    text = file.read()

tokenized_words = word_tokenize(text)
print("Tokenized words length:", len(tokenized_words))


def filter_words(words, stop_words):
    filtered_words = []
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)
    return filtered_words


stop_words = set(stopwords.words("english"))
filtered_words = filter_words(tokenized_words, stop_words)
print("Filtered words length:", len(filtered_words))

punctuation = [",", ".", ":", "'", "—", "[", "]", "(", ")", "{", "}", "!", "?", "’", "‘", "“", "”"]
for i in punctuation:
    stop_words.add(i)

filtered_words = filter_words(tokenized_words, stop_words)
print("Words length withour punctuation:", len(filtered_words))
print(filtered_words)

# from nltk.stem.wordnet import WordNetLemmatizer
# lem = WordNetLemmatizer()

stemmer = SnowballStemmer("english")

stemmed = []
for word in filtered_words:
    stemmed.append(stemmer.stem(word))

print("Length od stemmed words:", len(stemmed))

fd = nltk.FreqDist(stemmed)

## Creating FreqDist for whole BoW, keeping the 20 most common tokens
all_fdist = fd.most_common(20)

## Conversion to Pandas series via Python Dictionary for easier plotting
all_fdist = pd.Series(dict(all_fdist))

## Setting figure, ax into variables
fig, ax = plt.subplots(figsize=(10, 10))

## Seaborn plotting using Pandas attributes + xtick rotation for ease of viewing
all_plot = sns.barplot(x=all_fdist.index, y=all_fdist.values, ax=ax)
plt.xticks(rotation=30)
plt.show()
plt.close()

# Generate a word cloud image
wordcloud = WordCloud(width=800, height=400).generate(' '.join(stemmed))
# lower max_font_size
# wordcloud = WordCloud(width=800, height=400, max_font_size=60).generate(' '.join(stemmed))
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.close()

