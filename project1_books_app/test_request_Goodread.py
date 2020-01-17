import requests
import os

API_KEY = os.getenv('API_KEY')

res = requests.get("https://www.goodreads.com/book/review_counts.json",
             params={"key": API_KEY, "isbns": "9781632168146"})
print(res.json())