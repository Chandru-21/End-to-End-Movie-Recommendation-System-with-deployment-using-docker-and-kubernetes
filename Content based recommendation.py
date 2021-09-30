# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 09:45:32 2021

@author: Chandramouli
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle



data=pd.read_excel("movie data_new.xlsx")
data.info()
data.rename(columns={'Unnamed: 0': 'movie_id'}, inplace=True)

columns=['Cast','Director','Genre','Title','Description']


data[columns].isnull().values.any()#no null values

def get_important_features(data):
    important_features=[]
    for i in range (0,data.shape[0]):
        important_features.append(data['Title'][i]+' '+data['Director'][i]+' '+data['Genre'][i]+' '+data['Description'][i])
    return important_features


#creating a column to hold the combined strings
data['important_features']=get_important_features(data)


tfidf = TfidfVectorizer(stop_words='english')
#data['Description'] = data['Description'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['important_features'])
tfidf_matrix.shape


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


indices = pd.Series(data.index, index=data['Title']).drop_duplicates()
#indices['Stillwater']
#sim_scores = list(enumerate(cosine_sim[indices['Stillwater']]))
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 5 most similar movies
    movies=data['Title'].iloc[movie_indices]
    id=data['movie_id'].iloc[movie_indices]
    dict={"Movies":movies,"id":id}
    final_df=pd.DataFrame(dict)
    final_df.reset_index(drop=True,inplace=True)
    return final_df


get_recommendations('Spider-Man: Far from Home')
#Stillwater
get_recommendations('Stillwater')

data.info()
new = data.drop(columns=['Year of Release','Watch Time','Genre','Movie Rating','Metascore of movie','Director','Cast','Votes','Description'])

pickle.dump(new,open('movie_list.pkl','wb'))
pickle.dump(cosine_sim,open('similarity.pkl','wb'))
