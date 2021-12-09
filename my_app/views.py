import requests
from django.shortcuts import render
from bs4 import BeautifulSoup as bs
from requests.compat import quote_plus
from . import models


BASE_MEROSECONDHAND_URL = 'https://www.merosecondhand.com/search/pattern,{}'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_MEROSECONDHAND_URL.format(quote_plus(search))

    response = requests.get(final_url)

    data = response.text  #simple-prod o1...

    soup = bs(data, features='html.parser')


    post_listing = soup.find_all('div',{'class': 'simple-prod'})

    final_posting = []

    for post in post_listing:
        wrap = post.find('div', {'class':'simple-wrap'})
        post_title = wrap.find('a', {'class':'title'}).text
        post_url =wrap.find('a', {'class':'title'}).get('href')
        wrap_price = wrap.find('div', {'class':'price'})
        post_price = wrap_price.find('span').text
        item_img = wrap.find('div', {'class':'item-img-wrap'})
        anchor_image = item_img.find('a', {'class':'img-link'})
        post_image = anchor_image.find('img', {'class':'lazy'}).get('src')


        final_posting.append((post_title,post_url,post_price,post_image))

    stuff_for_frontend = {
                'search':search,
                'final_posting':final_posting,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
