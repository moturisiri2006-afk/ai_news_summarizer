import json

def save_news(articles):
    with open("data/news.json","w") as file:
        json.dump(articles,file,indent=4)

def read_news():
    with open("data/news.json","r") as file:
        articles = json.load(file)
        return articles