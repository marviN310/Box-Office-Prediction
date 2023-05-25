# Box-Office-Prediction
Web Scraping of movie data from Wikipedia and IMDB

Deployment of simple boosted tree model to predict Box-Office using Streamlit

## Files
+ scrap_wiki_utils.py: Functions to use for scraping data from wikipedia and IMDB
+ create_data.py: Script which collects the data from American movies from 2010 - 2022 (excluding,2020+2021)
+ data_preprocessing_utils.py : Function to use for preprocessing the unstructured data gather from create_data.py
+ data_preprocessing.py : Script which does the preprocessing of the data
+ boost_model.py : Fitting XGBoost model on data and saving the model
+ streamlit_app.py : Script to build streamlit application
+ requirements.txt : Requirements for streamlit application

## Summary of project

In the first step we scrap data from wikipedia pages of movies. We especially scrap data from
the info tables of the pages. Following variables are considered

+ Running time (in Minutes)
+ Genre of movie (multiple possible) 
+ Distribution company
+ Release month
+ Age Rating (using MPAA rating system)
