import requests
from django.http import HttpResponse
from django.shortcuts import render
from .models import Anime
from .models import Manga
from .models import Visit
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#informations sur anime et manga tiré de l'API Jikan
def anime_list(request):
    url = "https://api.jikan.moe/v4/top/anime"
    response = requests.get(url)
    data = response.json()
    anime_data = data["data"][:6]

    for anime in anime_data:
        title = anime["title"]
        image_url = anime['images']['jpg']['large_image_url']
        synopsis = anime["synopsis"][0:180]
        if not Anime.objects.filter(title=title).exists():
            Anime.objects.create(title=title, image_url=image_url, synopsis=synopsis)

    url2 = "https://api.jikan.moe/v4/top/manga"
    response2 = requests.get(url2)
    data2 = response2.json()
    manga_data = data2["data"][:6]

    for manga in manga_data:
        title2 = manga["title"]
        image_url2 = manga['images']['jpg']['large_image_url']
        synopsis2 = manga["synopsis"][0:180]
        if not Manga.objects.filter(title2=title2).exists():
            Manga.objects.create(title2=title2, image_url2=image_url2, synopsis2=synopsis2)

    manga_objects = Manga.objects.all()
    anime_objects = Anime.objects.all()
    
    return render(request, 'anime/anime_list.html', {'anime_list': anime_objects[::-1], 'manga_list': manga_objects[::-1]})

#informations sur les visites, l'ip et le user agent
def dark(request):
    visit = Visit.objects.create()
    visit_objects = Visit.objects.order_by('-date')[:5]

    visitor_ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    visit.visitor_ip = visitor_ip
    visit.user_agent = user_agent
    visit.save()
#informations sur la géolocalisation grâce à l'API ipinfo
    url = "http://ipinfo.io/176.182.219.208?token=dd9c8e94d6c24d"
    response = requests.get(url)
    if response.status_code == 200:
        location_data = response.json()
        country = location_data['country']
        city = location_data['city']
        org = location_data['org']
    else:
        country = city = org = None

    context = {
        'visit_counter': Visit.objects.count(),
        'visit_date': visit_objects,
        'visit_ip': visitor_ip,
        'visit_user_agent' : user_agent,
        'country': country,
        'city': city,
        'org': org
    }
    return render(request, 'anime/dark.html', context)
#Aller chercher la dernière news avec Selenium en passant sur le site web MyAnimeList
def button(request):
    response = requests.get("https://myanimelist.net/")
    if response.status_code != 200:
        print("première requête échouée ", response.status_code)
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find("h3", class_="title news_h3")
    url = link.find("a", href=True)["href"]
    print(url)
    response = requests.get(url)  
    if response.status_code != 200:
        print("seconde requête échouée ", response.status_code)
        return None
    #extraire uniquement le texte de la news
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.find("div", class_="content clearfix")
    text = news.get_text(strip=True)[:1000]

    return HttpResponse(text)