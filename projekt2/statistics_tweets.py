import json
from datetime import datetime, timedelta

tweets = []

with open("tweets.json", "r") as f:
    tweets = json.loads(f.read())


def count_by_day(tw):
    results = {}
    for t in tw:
        date = t["date"][:10]

        if date in results:
            results[date] += 1
        else:
            results[date] = 1

    return results


def count_by_week(tw):
    results = {}

    for t in tw:
        date = t["date"][:10]
        dt = datetime.strptime(date, '%Y-%m-%d')
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)

        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')
        week = start_str + "_" + end_str

        if week in results:
            results[week] += 1
        else:
            results[week] = 1

    return results


def count_by_month(tw):
    results = {}

    for t in tw:
        date = t["date"][:10]
        month = date[5:7]

        if month in results:
            results[month] += 1
        else:
            results[month] = 1

    return results


days = count_by_day(tweets)
weeks = count_by_week(tweets)
months = count_by_month(tweets)


def sort_dic_by_value(mydic, order=True):
    result = dict(sorted(mydic.items(), reverse=order, key=lambda item: item[1]))
    return result


days_sorted = sort_dic_by_value(days)
weeks_sorted = sort_dic_by_value(weeks)
months_sorted = sort_dic_by_value(months)
print(days_sorted)
print(weeks_sorted)
print(months_sorted)
