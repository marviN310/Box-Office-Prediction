import xgboost as xgb
import streamlit as st
import pandas as pd
import numpy as np

# Loading up the Regression model we created
model = xgb.XGBRegressor()
model.load_model('xgb_model_cv.json')

# Caching the model for faster loading


# Feature column expected by model
features = model.get_booster().feature_names


# Converting string output to one-hot encoding for model input


def encoding_category(category, list):
    indices = [i for i, element in enumerate(list) if category in element]

    one_hot = np.eye(len(list))[indices]

    return one_hot.tolist()[0]


# Categories (order important)

genres_categories = ['Action',
                     'Adventure',
                     'Animation',
                     'Biography',
                     'Comedy',
                     'Crime',
                     'Documentary',
                     'Drama',
                     'Family',
                     'Fantasy',
                     'History',
                     'Horror',
                     'Music',
                     'Musical',
                     'Mystery',
                     'Romance',
                     'Sci-Fi',
                     'Sport',
                     'Thriller',
                     'War',
                     'Western']

company_categories = ['Distribution company_20th Century Studios',
                      'Distribution company_A24',
                      'Distribution company_Amazon Studios',
                      'Distribution company_Bleecker Street',
                      'Distribution company_CBS Films',
                      'Distribution company_Entertainment One',
                      'Distribution company_FilmDistrict',
                      'Distribution company_Focus Features',
                      'Distribution company_Freestyle Releasing',
                      'Distribution company_IFC Films',
                      'Distribution company_Lionsgate',
                      'Distribution company_Magnet Releasing',
                      'Distribution company_Magnolia Pictures',
                      'Distribution company_Neon',
                      'Distribution company_Netflix',
                      'Distribution company_Open Road Films',
                      'Distribution company_Other',
                      'Distribution company_Paramount Pictures',
                      'Distribution company_Pure Flix Entertainment',
                      'Distribution company_Relativity Media',
                      'Distribution company_Roadside Attractions',
                      'Distribution company_STXfilms',
                      'Distribution company_Saban Films',
                      'Distribution company_Searchlight Pictures',
                      'Distribution company_Sony Pictures Classics',
                      'Distribution company_Sony Pictures Releasing',
                      'Distribution company_StudioCanal',
                      'Distribution company_Summit Entertainment',
                      'Distribution company_The Weinstein Company',
                      'Distribution company_United Artists Releasing',
                      'Distribution company_Universal Pictures',
                      'Distribution company_Vertical Entertainment',
                      'Distribution company_Walt Disney Studios',
                      'Distribution company_Warner Bros. Pictures']

months = ['Release month_April',
          'Release month_August',
          'Release month_December',
          'Release month_February',
          'Release month_January',
          'Release month_July',
          'Release month_June',
          'Release month_March',
          'Release month_May',
          'Release month_November',
          'Release month_October',
          'Release month_September']

ratings = ['Age Rating_G',
             'Age Rating_NC-17',
             'Age Rating_Not Rated',
             'Age Rating_PG',
             'Age Rating_PG-13',
             'Age Rating_R']


def predict(runningtime, budget, company, month, genres, rating):
    #genres_one_hot = encoding_category(genres, genres_categories)
    company_one_hot = encoding_category(company, company_categories)
    month_one_hot = encoding_category(month, months)
    #ratings_one_hot = encoding_category(rating, ratings)
    
    if rating=="G":
       ratings_one_hot = [1,0,0,0,0,0]
    elif rating=="PG":
       ratings_one_hot = [0,0,0,1,0,0]
    elif rating=="PG-13":
       ratings_one_hot = [0,0,0,0,1,0]  
    elif rating=="R":
       ratings_one_hot = [0,0,0,0,0,1]  
    elif rating=="NC-17":
       ratings_one_hot = [0,1,0,0,0,0]
    elif rating=="Not Rated":
       ratings_one_hot = [0,1,0,0,0,0]    
    
    if type(genres) == list:
        list_one_hot = [encoding_category(genre, genres_categories) for genre in genres]
                        
        genres_one_hot = np.sum(list_one_hot, axis=0).tolist()
        
    else:
        genres_one_hot = encoding_category(genres, genres_categories)

        
        
    all_list = [runningtime] + [budget] + genres_one_hot + company_one_hot + month_one_hot + ratings_one_hot
    prediction = model.predict(pd.DataFrame([all_list], columns=features))
    return prediction


st.title('Box Office Predictor')

runningtime = st.slider('Running time in minutes', 60, 250, 100)

# Streamlit number
budget = st.slider('Budget in Mio $', 0, 500, 20)

company = st.selectbox('Distribution company:', ['20th Century Studios',
                                                 'A24',
                                                 'Amazon Studios',
                                                 'Bleecker Street',
                                                 'CBS Films',
                                                 'Entertainment One',
                                                 'FilmDistrict',
                                                 'Focus Features',
                                                 'Freestyle Releasing',
                                                 'IFC Films',
                                                 'Lionsgate',
                                                 'Magnet Releasing',
                                                 'Magnolia Pictures',
                                                 'Neon',
                                                 'Netflix',
                                                 'Open Road Films',
                                                 'Paramount Pictures',
                                                 'Pure Flix Entertainment',
                                                 'Relativity Media',
                                                 'Roadside Attractions',
                                                 'STXfilms',
                                                 'Saban Films',
                                                 'Searchlight Pictures',
                                                 'Sony Pictures Classics',
                                                 'Sony Pictures Releasing',
                                                 'StudioCanal',
                                                 'Summit Entertainment',
                                                 'The Weinstein Company',
                                                 'United Artists Releasing',
                                                 'Universal Pictures',
                                                 'Vertical Entertainment',
                                                 'Walt Disney Studios',
                                                 'Warner Bros. Pictures', 'Other'])

month = st.selectbox('Release month:', ['January',
                                        'February',
                                        'March',
                                        'April',
                                        'May',
                                        'June',
                                        'July',
                                        'August',
                                        'September',
                                        'October',
                                        'November',
                                        'December'])

genres = st.multiselect("Genres:", ['Action',
                                  'Adventure',
                                  'Animation',
                                  'Biography',
                                  'Comedy',
                                  'Crime',
                                  'Documentary',
                                  'Drama',
                                  'Family',
                                  'Fantasy',
                                  'History',
                                  'Horror',
                                  'Music',
                                  'Musical',
                                  'Mystery',
                                  'Romance',
                                  'Sci-Fi',
                                  'Sport',
                                  'Thriller',
                                  'War',
                                  'Western'])

rating = st.selectbox("Age Rating:", ["G","PG","PG-13","R","NC-17",
                                       "Not Rated"])


if st.button('Predict Box Office'):
    price = predict(runningtime, budget, company, month, genres, rating)
    st.success(f'The predicted Box Office is ${int(price[0])} Mio USD')
