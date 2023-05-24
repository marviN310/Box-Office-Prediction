# Import libraries

import ast
import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer


def money_handling(string):
    if pd.isna(string):
        return string
    else:
        if "mil" in string:
            match = re.search(r'\d+', string)

            if match:
                number = float(match.group())
            return number
        elif "bil" in string:
            match = re.search(r'\d+', string)

            if match:
                number = float(match.group())
            return number * 1000
        elif "₹" in string:
            return string

        else:
            match = re.sub(r'[^\d.]', '', string)
            if match.isalpha() or len(match) == 0 or "." in string:
                return string
            elif len(string) <= 7 or "–" in string:
                match = re.search(r'\d+', string)

                if match:
                    number = float(match.group())
                return number

            else:
                number = float(match)
                number = number / 1000000
                return number


def runtime_handling(runtime):
    if pd.isna(runtime):
        return runtime
    else:
        time = runtime.split("min")[0].strip()
        return float(time)


def data_preprocess(movie_data):
    # Filter movies out without Box office
    movie_data_filtered = movie_data.dropna(subset=['Box office'], ignore_index=True)

    ##Distribution company
    # Remove (..) in strings

    movie_data_filtered["Distribution company"] = movie_data_filtered["Distribution company"].apply(
        lambda x: x.split("(")[0].strip() if pd.notna(x) else x)

    # Remove [..] in strings
    movie_data_filtered["Distribution company"] = movie_data_filtered["Distribution company"].apply(
        lambda x: x.split("[")[0].strip() if pd.notna(x) else x)

    # Assign movie studios to movie studio which is similar/same

    disney_to_assign = 'Walt Disney Studios'
    disney_to_replace = ['Walt Disney Studios Motion Pictures', 'Walt Disney StudiosMotion Pictures',
                         'Walt Disney Studios Motion Pictures Finland']
    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        disney_to_replace, disney_to_assign)

    searchlight_to_assign = 'Searchlight Pictures'
    searchlight_to_replace = "Fox Searchlight Pictures"
    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        searchlight_to_replace, searchlight_to_assign)

    stx_to_assign = "STXfilms"
    stx_to_replace = "STX Entertainment"
    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        stx_to_replace, stx_to_assign)

    lions_to_assign = "Lionsgate"
    lions_to_replace = ["Lionsgate Premiere", 'Lionsgate Films', "'Lionsgate UK'"]

    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        lions_to_replace, lions_to_assign)

    thcentury_to_assign = "20th Century Studios"
    thcentury_to_replace = "20th Century Fox"

    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        thcentury_to_replace, thcentury_to_assign)

    warner_to_assign = "Warner Bros. Pictures"
    warner_to_replace = ['Warner Bros. España', 'Warner Bros. Entertainment España', 'Warner Bros. France',
                         'Warner Bros.']
    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'].replace(
        warner_to_replace, warner_to_assign)

    # Summarize rest
    rare_categories = movie_data_filtered['Distribution company'].value_counts()[movie_data_filtered
                                                                                 [
                                                                                     'Distribution company'].value_counts() < 8].index
    movie_data_filtered['Distribution company'] = movie_data_filtered['Distribution company'] \
        .apply(lambda x: 'Other' if x in rare_categories else x)

    ##Budget

    # Converting budget string to near-float string
    movie_data_filtered["Budget"] = movie_data_filtered["Budget"].apply(money_handling)

    # Remove remaining strings
    movie_data_filtered["Budget"] = pd.to_numeric(movie_data_filtered["Budget"], errors='coerce')

    # Handle miscalenaous cases (from imdb)

    movie_data_filtered.loc[movie_data_filtered['Title'] == "Little Italy", "Budget"] = 6
    movie_data_filtered.loc[movie_data_filtered['Title'] == "Tim and Eric's Billion Dollar Movie", "Budget"] = 3

    ##Box Office

    # Converting budget string to near-float string
    movie_data_filtered["Box office"] = movie_data_filtered["Box office"].apply(money_handling)
    # Remove remaining strings
    movie_data_filtered["Box office"] = pd.to_numeric(movie_data_filtered["Box office"], errors='coerce')

    # Handle #Handle miscalenaous cases (from imdb)

    movie_data_filtered.loc[movie_data_filtered['Title'] == "Red Riding Hood", "Box office"] = 90
    movie_data_filtered.loc[movie_data_filtered['Title'] == "5 Broken Cameras", "Box office"] = 0.1
    movie_data_filtered.loc[movie_data_filtered['Title'] == "Dragon Ball Z: Battle of Gods", "Box office"] = 50

    ##Running time

    # Converting budget string to near-float string
    movie_data_filtered["Running time"] = movie_data_filtered["Running time"].apply(runtime_handling)

    ##Genres

    # Convert string to lists
    movie_data_filtered["Genres"] = movie_data_filtered["Genres"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else x)

    # Multi label encoding

    # Replace NaN values with None
    movie_data_filtered["Genres"].fillna(value="", inplace=True)

    # Instantiate MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    # Transform the 'genres' column into binary columns using fit_transform
    genres_encoded = pd.DataFrame(mlb.fit_transform(movie_data_filtered["Genres"]),
                                  columns=mlb.classes_,
                                  index=movie_data_filtered.index)

    # Concat data frames

    movie_data_filtered = pd.concat([movie_data_filtered, genres_encoded], axis=1).drop(["Genres"], axis=1)

    # filter out again nan values

    movie_data_filtered = movie_data_filtered.dropna(subset=['Box office'], ignore_index=True)

    # Other data preproccesing steps
    # One hot encoding other categorical variables
    movie_data_filtered = pd.get_dummies(movie_data_filtered,
                                         columns=["Distribution company", "Release month", "Age Rating"],
                                         drop_first=True)
    # Converting bool to int

    movie_data_filtered = movie_data_filtered.replace({True: 1, False: 0})

    return movie_data_filtered




movie_data = pd.read_csv("full_movie_data.csv")

movie_data_new = data_preprocess(movie_data)

print(movie_data_new.info())

movie_data_new.to_csv('full_movie_data_processed.csv', index=False)  # Save dataframe as csv
