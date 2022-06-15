import json

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from PIL import Image
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, ImageColorGenerator

nltk.download('vader_lexicon')

from util import filter_words
from util import lemmatize_words

tweets = []

with open("tweets.json", "r") as f:
    tweets = json.loads(f.read())

text = []
positive = 0
positive_list = []
negative = 0
negative_list = []
neutral = 0
neutral_list = []
stop_words = set(stopwords.words("english"))

punctuation = [",", ".", ":", "'", "—", "[", "]", "(", ")", "{", "}", "!", "?", "’", "‘", "“", "”", "…"]
for i in punctuation:
    stop_words.add(i)

sid = SentimentIntensityAnalyzer()

for tweet in tweets:

    # if (tweet["date"][5:7] != "06"):
    #     continue

    content = tweet["content"]
    string_encode = content.encode("ascii", "ignore")
    string_decode = string_encode.decode()
    tweet_list = string_decode.split()
    tweet_list = [x for x in tweet_list if not x.startswith(('#', 'http', '\\', '&', '"Article Link:',
                                                             "(Source:", 'via', 'via @'))]
    tokenized = word_tokenize(' '.join(tweet_list))
    tokenized = list(map(lambda word: word.lower().strip(), tokenized))
    filtered = filter_words(tokenized, stop_words)
    lem = lemmatize_words(filtered)

    text.extend(lem)
    tweet_text = ' '.join(lem)
    ss = sid.polarity_scores(tweet_text)

    if ss["compound"] < 0:
        negative += 1
        negative_list.append(tweet_text)
    elif ss["compound"] > 0:
        positive += 1
        positive_list.append(tweet_text)
    else:
        neutral += 1
        neutral_list.append(tweet_text)


print(negative, neutral, positive)

with open("tweets_negative.txt", "w") as f:
    for i, t in enumerate(negative_list):
        if i == 100:
            break
        f.write(t + "\n")

with open("tweets_neutral.txt", "w") as f:
    for i, t in enumerate(positive_list):
        if i == 100:
            break
        f.write(t + "\n")

with open("tweets_positive.txt", "w") as f:
    for i, t in enumerate(positive_list):
        if i == 100:
            break
        f.write(t + "\n")

ss = sid.polarity_scores(' '.join(text))

print(ss)

# l2 = [x.split() for x in neutral_list]
# l3 = [item for sublist in l2 for item in sublist]
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
plt.savefig('graphs/fd.png')
plt.show()
plt.close()


country_mask = np.array(Image.open("ua-02.png"))

# Generate a word cloud image
wordcloud = WordCloud(width=1200, height=675, background_color="#000", mask=country_mask,
                      contour_width=1, contour_color='blue', max_font_size=48, max_words=200)

wordcloud.generate(' '.join(text))

# create coloring from image
image_colors = ImageColorGenerator(country_mask)

# display wordcloud
plt.figure(figsize=(16, 9))
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.savefig('graphs/wc.png', bbox_inches='tight')
plt.show()
plt.close()
