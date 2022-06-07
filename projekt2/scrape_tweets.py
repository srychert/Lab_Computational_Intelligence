import json

import snscrape.modules.twitter

tweets = []

scraper = snscrape.modules.twitter.TwitterSearchScraper('#ukraine #war” since:2022-02-20')
for i, tweet in enumerate(scraper.get_items()):
    if i > 30000:
        print(tweet.date)
        break
    if (tweet.lang == "en"):
        tweets.append({"content": tweet.content, "date": tweet.date})

with open("tweets.json", "w") as f:
    f.write(json.dumps(tweets, indent=4, default=str))
