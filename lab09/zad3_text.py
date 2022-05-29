import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

review_positive = '''
The apartment is beautiful, modern and very clean and well maintained.
The host is lovely and communication with him is great.
The location is very close to the main attractions.
Gdansk is a very pretty place. The beds were all very nice and comfortable.
Bathroom was very clean and modern, lovely shower. Would definitely recommend anyone to stay here.
'''

review_negative = '''
My closet is bigger than the bathroom. The sink was super tiny and you had to worry about hitting your head on the rack
above the sink. The bathroom was so small that my arm nearly got cut by the corner of the rack above the sink.
My wife has long hair and she had difficulty washing her hair under the shower. It was a very small shower.
A bigger person would not fit in the shower. The only normal thing about the bathroom was the toilet.
And never in my life did I have to beg the staff for more toilet paper. They didn't provide even one extra roll.
Towels were dirty, not all of them, but during our stay we had towels with spots on them.
The room was tiny as well and had an old smell to it. Probably because the carpet hasn't been changed in a long time.
We had to keep our windows open and it wasn't convenient because of the constant noise from the train tracks.
Bed sheets were fine but no fridge.'''


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]


reviews = [review_positive, review_negative]

for review in reviews:
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(review)
    print("{name}:".format(name=namestr(review, globals())[0]))
    for k in sorted(ss):
        print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
