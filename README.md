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

## Data Extraction

In the first step we scrap data from wikipedia pages of movies using **wikipedia API** and **beautiful soup**. We especially scrap data from
the info tables of the pages. Following variables are considered

+ Running time (in Minutes)
+ Genre of movie (multiple possible) 
+ Distribution company
+ Release month
+ Age Rating (using MPAA rating system)
+ Budget in Mio $
+ Worldwide Box Office in Mio $

In the next step we create our dataset. 
We focussed on cinema releases in America and herefore gathered the movie pages from the
"List of American films of **year**" page on wikipedia.
We collected data of cinema releases in America from *2010* to *2022* ,excluding 2020 and 2021 due to COVID effects.
After data cleaning and processing with **pandas**  we get a dataframe with 1979 movies.

## Prediction model

The idea is to predict the Box Office Variable, using these variables as predictors
+ Running time (in Minutes)
+ Genre of movie (multiple possible) 
+ Distribution company
+ Release month
+ Age Rating (using MPAA rating system)
+ Budget in Mio $

We choose as the prediction algorithm a **XGBoost** regressor and finetuned the hyperparameters using GridSearchCV.
Since the number of observations of our data is not big, we evaluate the model using *Cross-Fold-Validation with* 5 folds.
Because of the high skewness of the Box-Office variable, our performance metric is the *MAE* (Mean Absolute Error).

+ The MAE of the 5 folds has a mean of approx. 67 Mio $ and a standard deviation of approx. 6 Mio $

## Streamlit application
We then build a streamlit application trained on the whole 1979 movies.

