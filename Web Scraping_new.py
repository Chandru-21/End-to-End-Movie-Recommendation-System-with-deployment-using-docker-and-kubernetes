# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 12:30:20 2021

@author: Chandramouli
"""

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup



headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
           'Accept-Language': 'en-US, en;q=0.5'})


movie_name = []
year = []
time=[]
rating=[]
metascore =[]
director=[]
votes = []
gross = []
description = []
genre=[]

pages = np.arange(1,1000,50)
#https://www.imdb.com/search/title/?title_type=feature&primary_language=en
#https://www.imdb.com/search/title/?title_type=feature&primary_language=en&start=51&ref_=adv_nxt
for page in pages:
   
    page = requests.get("https://www.imdb.com/search/title/?title_type=feature&primary_language=en&start="+str(page)+"&ref_=adv_nxt")
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
    for store in movie_data:
        name = store.h3.a.text
        movie_name.append(name)
        
        year_of_release = store.h3.find('span', class_ = "lister-item-year text-muted unbold").text.replace('(', '')
        year_of_release=year_of_release.replace(')','')
        year.append(year_of_release)
        
        runtime = store.p.find("span", class_ = 'runtime').text if store.find('span', class_ = "runtime") else "NA"
        time.append(runtime)
        
        gen = store.p.find("span", class_ = 'genre').text
        genre.append(gen)
        
        rate = store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', '') if store.find('div', class_ = "inline-block ratings-imdb-rating") else "NA"
        rating.append(rate)
        #rate = store.find('div', class_ = "ratings-bar").find('strong').text.replace('\n', '')
        #rating.append(rate)
        
        meta = store.find('span', class_ = "metascore").text if store.find('span', class_ = "metascore") else "NA"#if meta score not present then *
        
        metascore.append(meta)
        
        #dire=store.find('p',class_ = "metascore")
        dire=store.find('p',class_='').find_all('a')[0].text
        
        director.append(dire)
        
        
        value = store.find_all('span', attrs = {'name':'nv'}) if store.find_all('span', attrs = {'name':'nv'}) else 'NA'
        vote = value[0].text if store.find_all('span', attrs = {'name':'nv'}) else 'NA'

        #vote = value[0].text if len(value)>1 else 'NA'
        votes.append(vote)
        
        #grosses = value[1].text if len(value)>1 else 'NA'
        #gross.append(grosses)
        
      
        describe = store.find_all('p', class_ = 'text-muted')
        description_ = describe[1].text.replace('\n', '') if len(describe) >1 else 'NA'
        description.append(description_)
        
#dataframe
movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Watch Time": time,"Genre":genre,"Movie Rating": rating, "Metascore of movie": metascore,"Director":director,"Votes" : votes,"Description": description})
movie_list.to_excel("movie data_new.xlsx")