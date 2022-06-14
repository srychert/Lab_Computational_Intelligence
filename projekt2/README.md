# Analiza Tweetów z hasztagami: "#war #ukraine"

## Dane
<p>Zebrano tweety od <b>2022-01-01</b> do <b>2022-06-14</b>. Zachowano wyłacznie tweety, których język był oznaczony jako angielski. Łączona liczba uzyskanych tweetów: <b>110845</b></p>

```python
scraper = snscrape.modules.twitter.TwitterSearchScraper('#ukraine #war” since:2022-01-01')
for i, tweet in enumerate(scraper.get_items()):
    if (tweet.lang == "en"):
        tweets.append({"content": tweet.content, "date": tweet.date})

with open("tweets.json", "w") as f:
    f.write(json.dumps(tweets, indent=4, default=str))
```

## Obróbka danych
<p>Z Każdego tweeta usunięto znaki specialne, a następnie poddano tokenizacji, filtracji oraz lematyzacja. Efekty te zostały uzyskane za pomocą biblioteki nltk.</p>

```python
content = tweet["content"]
string_encode = content.encode("ascii", "ignore")
string_decode = string_encode.decode()
tweet_list = string_decode.split()
tokenized = word_tokenize(' '.join(tweet_list))
tokenized = list(map(lambda word: word.lower().strip(), tokenized))
filtered = filter_words(tokenized, stop_words)
lem = lemmatize_words(filtered)
```

## Rozkład częstotliwości słów
<p>Odpowiednio przygotowane tweety zostały połączone w jeden duży tekst, w którym sprawdzony częstotliwość występowania słów. Poniższy wykres przestawia 10 najczęściej pojawiających się słów.</p>

![ScreenShot](projekt2/graphs/FreqDistAll.PNG) <br/>
![ScreenShot](projekt2/graphs/WordCloud.PNG) <br/>

## Analiza opinii
<p>Przeprowadzono analizę opinii ("sentymentu") z wykorzystaniem modułu Vader z biblioteki nltk. Analizie poddany został każdy twett z osobna jak i całość tekstu. </p>

```python
sid = SentimentIntensityAnalyzer()
ss = sid.polarity_scores(tweet_text)
#...
ss_all = sid.polarity_scores(' '.join(text))
```

### Wyniki
- {'neg': 0.242, 'neu': 0.618, 'pos': 0.14, 'compound': -1.0}
- Negatywne: 55919
- Neutralne: 25794
- Pozytywne: 29132 

<p>Narzędzie zakwalifikowało całość tweetów jako wypowiedzi negatywne na tematy związane z hasztagami #war #ukraine</p>


## Wydarzenia a liczba tweetów
<p>Przeprowadzono zliczenie ilości tweetów w odstępach czasowych: "dzień", "tydzień", "miesiąc". <br />
</p>

### Dni z największą liczbą tweetów
- 2022-02-24: 4718
- 2022-02-27: 2840
- 2022-02-26: 2776
- 2022-02-28: 2422

### Tygodnie z największą liczbą tweetów
- 2022-02-21_2022-02-27: 14885
- 2022-02-28_2022-03-06: 13758
- 2022-03-07_2022-03-13: 9080
- 2022-03-14_2022-03-20: 8821

### Miesiące
- 03: 40623
- 04: 26510
- 02: 19314
- 05: 17888
- 06: 5274
- 01: 1236}

Wniosek: Najwięcej tweetów pojawiło się w momencie rozpoczącie inwazji Rosji na Ukrainę dnia 24 lutego 2022 roku.


