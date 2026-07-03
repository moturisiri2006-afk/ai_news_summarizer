base_url = "https://newsapi.org/v2"
endpoint = "/top-headlines"

country = "in"
category = "technology"

url = f"{base_url}{endpoint}?country={country}&category={category}"

print(url)