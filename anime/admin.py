from django.contrib import admin
from .models import Anime
from .models import Manga
from .models import Visit

admin.site.register(Anime)
admin.site.register(Manga)
admin.site.register(Visit)
