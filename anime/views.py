import requests
from django.shortcuts import render
from .models import Anime
from .models import Manga
from .models import Visit

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
    return render(request, 'anime/anime_list.html', {'anime_list': anime_objects, 'manga_list': manga_objects})

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