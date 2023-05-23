from django.urls import path
from news.views import scrape , news_list, worldnews, indianews
from django.conf.urls import url
from django.contrib import admin
#from .views import (searchposts)


#from.import views
urlpatterns = [
	
	path('scrape/',scrape, name="scrape"),
	path("",news_list, name="home"),
	path('worldnews',worldnews,name='worldnews'),
	path('indianews',indianews,name='indianews'),
    #url(r'^$', searchposts, name='searchposts'),
]