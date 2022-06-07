import json

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud

from util import filter_words
from util import lemmatize_words

tweets = []

with open("tweets.json", "r") as f:
    tweets = json.loads(f.read())

text = []
stop_words = set(stopwords.words("english"))

for tweet in tweets:
    tokenized = word_tokenize(tweet["content"])
    filtered = filter_words(tokenized, stop_words)
    lem = lemmatize_words(filtered)
    filtered2 = filter(lambda t: t != 'http', lem)

    text.extend(filtered2)

fd = nltk.FreqDist(text)

## Creating FreqDist for whole BoW, keeping the 10 most common tokens
all_fdist = fd.most_common(10)

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
wordcloud = WordCloud(width=800, height=450).generate(' '.join(text))
# lower max_font_size
# wordcloud = WordCloud(width=800, height=400, max_font_size=60).generate(' '.join(stemmed))
plt.figure(figsize=(16, 9))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.close()
