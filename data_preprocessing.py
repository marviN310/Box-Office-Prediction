from data_preprocessing_utils import *
import pandas as pd

# Import originally created data
movie_data = pd.read_csv("full_movie_data.csv")

# Preprocess data
movie_data_new = data_preprocess(movie_data)

# Save preprocessed data
movie_data_new.to_csv('full_movie_data_processed.csv', index=False)  # Save dataframe as csv
