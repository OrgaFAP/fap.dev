import requests


def range_date():
    url = "http://127.0.0.1:8000/data/range"
    data = {"items": ["2026-04-19", "2026-04-26"], "databases": ["Xvideos", "Pornhub"]}
    r = requests.post(url, data=data)
    print(r)
    print(r.text)


def date():
    url = "http://127.0.0.1:8000/data/by-date/?date=2026-04-29"
    r = requests.post(url)
    print(r)
    print(r.text)


date()
