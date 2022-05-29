from subprocess import call
import snscrape.modules.twitter

# To get the latest 100 tweets with the hashtag #MonkeypoxVirus:
call(["snscrape", "--max-results", "100", "--jsonl", "twitter-hashtag", "MonkeypoxVirus"])

scraper = snscrape.modules.twitter.TwitterSearchScraper('#MonkeypoxVirus since:2022-05-01 until:2022-05-29 near:"Gdańsk" within:"60km"')
for tweet in scraper.get_items():
	print("\n", tweet.json())

