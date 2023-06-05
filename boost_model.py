import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

# Import preprocessed data
movie_data_new = pd.read_csv("full_movie_data_processed.csv")



#Feature-Target split
movie_features = movie_data_new.drop(["Box office","Title"],axis=1)
target = movie_data_new["Box office"]

# Using GridSearch for hyperparameter tuning on XGBoost model

xgb_cl = XGBRegressor()

param_grid = {
    "max_depth": [3, 4, 5, 7],
    "learning_rate": np.arange(0.1, 0.6, 0.1),
    "n_estimators": [50, 60, 70, 80, 90, 100],
    "reg_lambda": [0, 1, 10],
    "subsample": [0.8, 1],
}

grid_cv = GridSearchCV(xgb_cl, param_grid, scoring="neg_mean_absolute_error")

#Train model

grid_cv.fit(movie_features, target)

#Save model
best_model = grid_cv.best_estimator_
best_model.save_model('xgb_model_cv.json')
