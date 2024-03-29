import requests

url = "https://api.jikan.moe/v4/anime/24"

reponse = requests.get(url)
contenu = reponse.json()
print(reponse)
print(contenu)
