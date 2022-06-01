from subprocess import call
import snscrape.modules.twitter
import json
from util import filter_words
from util import lemmatize_words
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')

# To get the latest 100 tweets with the hashtag #MonkeypoxVirus:
# call(["snscrape", "--max-results", "100", "--jsonl", "twitter-hashtag", "MonkeypoxVirus"])

tweets = []

# scraper = snscrape.modules.twitter.TwitterSearchScraper('#MonkeypoxVirus since:2022-05-01 until:2022-05-29 near:"Gdańsk" within:"60km"')
scraper = snscrape.modules.twitter.TwitterSearchScraper('#virus since:2020-06-01')
for i, tweet in enumerate(scraper.get_items()):
    if i > 10:
        break
    if (tweet.lang == "en"):
        tweets.append(tweet.content)

print(tweets[0])

with open("tweets.json", "w") as f:
    f.write(json.dumps(tweets, indent=4))

stop_words = set(stopwords.words("english"))

for content in tweets:
    tokenized = word_tokenize(content)
    filtered = filter_words(tokenized, stop_words)
    lem = lemmatize_words(filtered)

    print(lem)
