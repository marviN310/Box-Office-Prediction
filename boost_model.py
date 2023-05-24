import pandas as pd
from xgboost import XGBRegressor


# Import preprocessed data
movie_data_new = pd.read_csv("full_movie_data.csv")



#Feature-Target split
movie_features = movie_data_new.drop(["Box office","Title"],axis=1)
target = movie_data_new["Box office"]

# Use simple XGBoost model for prediction

xgb_cl = XGBRegressor()

xgb_cl.fit(movie_features, target)
