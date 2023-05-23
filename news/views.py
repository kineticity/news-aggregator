from django.shortcuts import render
from django.db import IntegrityError
# Create your views here.

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline,Headline1
#from news.models import worldHeadline
from django.db import connection


Headline.objects.all().delete()
#Headline1.objects.all().delete()


cursor=connection.cursor()
cursor.execute('SELECT*FROM news_headline1 where category="India"')
huh=cursor.fetchall()
##print("huh")
#print(huh)

#headlines = Headline1.objects.filter(category='World')
#print(headlines)
def worldnews(request):
	headlines = Headline1.objects.filter(category='World')[::-1]
	context ={
		"worldobject_list": headlines,
	}

	return render(request , "news/worldnews.html",context)

def indianews(request):
	headlines = Headline1.objects.filter(category='India')[::-1]
	context ={
		"object_list": headlines,
	}

	return render(request , "news/indianews.html",context)


def news_list(request):
	headlines = Headline1.objects.all()[::-1]
	context ={
		"object_list": headlines,
	}

	return render(request , "news/home.html",context)

'''def worldnews_list(request):
	headlines = worldHeadline.objects.all()[::-1]
	context ={
		"object_list": worldheadlines,
	}

	return render(request , "news/worldnews.html",context)'''


def scrape_ht(url_ht,session):

	content_ht=session.get(url_ht, verify=False).content
	soup_ht = BSoup(content_ht,"html.parser")
	News_ht = soup_ht.find_all('div',{"class": "cartHolder listView"})
	if url_ht=="https://www.hindustantimes.com/world-news":
		category="World"
	elif url_ht=="https://www.hindustantimes.com/india-news":
		category="India"

	for article in News_ht:
		image_url = article.find('figure').span.a.img['src']
		title=article.find('h3',{"class": "hdg3"}).a.text
		link =str(url_ht[:-10]+article.find('h3',{"class": "hdg3"}).a['href'])
		try:
			description = str(article.find('div',{"class": "sortDec"}).text)
		except:
			description = str(article.find('div',{"class": "sortDec"}))
		#category=article.find('div',{"class":"catName pt10"}).a.text
		
		new_headline = Headline1()
		new_headline.title = title
		new_headline.url = link
		new_headline.image = image_url
		new_headline.description= description
		new_headline.category=category

		try:
			new_headline.save()
		
		except IntegrityError as e: 
			if 'unique constraint' in e.args:
				continue 

    


        
                    
		
def scrape_it(url,session):
	content = session.get(url, verify=False).content
	soup = BSoup(content,"html.parser")
    #News = soup.find_all('div',{"class": "view-content"})

    #for article in News:
	if url=="https://www.indiatoday.in/world":
		category="World"
	elif url=="https://www.indiatoday.in/india":
		category="India"
	
	News = soup.find_all('div',{"class": "catagory-listing"})

	for article in News:
	
		image_url = article.find('div',{"class": "pic"}).img['src']
		title=  article.find('div',{"class": "detail"}).h2.a.contents[0]
		link = str(url[:-6]+article.find('div',{"class": "detail"}).h2.a['href'])
		try:
			description = str(article.find('div',{"class": "detail"}).p.text)
		except:
			description = str(article.find('div',{"class": "detail"}).p)


		new_headline = Headline1()
		new_headline.title = title
		new_headline.url = link
		new_headline.image = image_url
		new_headline.description= description
		new_headline.category=category

		try:
			new_headline.save()
		
		except IntegrityError as e: 
			if 'unique constraint' in e.args:
				continue 



def scrape(request):
	session = requests.Session()
	session.headers ={"User-Agent":"Googlebot/2.1 (+http://www.google.com/bot.html)"}
	scrape_ht("https://www.hindustantimes.com/world-news",session)
	scrape_ht("https://www.hindustantimes.com/india-news",session)

	
	scrape_it("https://www.indiatoday.in/world",session)
	scrape_it("https://www.indiatoday.in/india",session)

	#for page in range(1,5):
			#url+='?page=%d'%page
	return redirect("../")

'''
def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(content__icontains=query)

            results= Post.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search/search.html', context)

        else:
            return render(request, 'search/search.html')

    else:
        return render(request, 'search/search.html')'''



'''
def scrape_world(request):
	session = requests.Session()
	session.headers ={"User-Agent":"Googlebot/2.1 (+http://www.google.com/bot.html)"}
	scrape_ht("https://www.hindustantimes.com/world-news",session)
	 
	for i in range(len())

	scrape_it("https://www.indiatoday.in/world",session)



	return redirect("../")'''

