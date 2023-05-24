
from scrap_wiki_utils import *
import pandas as pd



def util_func(movie):

    try:
        return(get_wiki_moviedata(movie))
    except:
        pass


full_movie_data= []  #Initialize data list

years = ["2011","2012","2013","2014","2015","2016","2017","2018","2019","2022"]   #movie years in consideration

for year in years:
    print(year)
    movies_year = get_movie_titles(year)                                 
    movie_data = [util_func(movie) for movie in movies_year]             #Loop through year
    movie_data = [movie for movie in movie_data if movie is not None]    #Remove None values

    full_movie_data += movie_data


df = pd.DataFrame.from_records(full_movie_data)    #Create dataframe

df.to_csv('full_movie_data.csv', index=False)     #Save dataframe as csv






