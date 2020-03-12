import requests


def main():
    res = requests.get("https://finance.yahoo.com/quote/AMZN?p=AMZN")
    return print(res.text)


if __name__ == "__main__":
    main()
