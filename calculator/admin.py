from django.contrib import admin
from .models import News, iframeVideo, adsitem
# Register your models here.

@admin.register(News)
class adminNews(admin.ModelAdmin):
    list_news = ['title','descryption','date','website','link']

@admin.register(iframeVideo)
class adminVideo(admin.ModelAdmin):
    list_videos = ['title','video_url']

@admin.register(adsitem)
class adminAds(admin.ModelAdmin):
    list_ads = ['title', 'ad_url', 'ad_ref']
