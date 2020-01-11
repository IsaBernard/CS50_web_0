import requests

res = requests.get("https://www.goodreads.com/book/review_counts.json",
             params={"key": "rs0FMt22nijlGe2eBNP9Xg", "isbns": "9781632168146"})
print(res.json())