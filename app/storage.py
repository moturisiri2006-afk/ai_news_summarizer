import json

def save_news(articles):
    with open("data/news,json","w") as file:
        json.dump(articles,file,indent=4)
