

from bs4 import BeautifulSoup, Tag, NavigableString
import requests
import json


import datetime
import re
import sys
import wikipedia

import numpy as np
import pandas as pd


def get_movie_titles(year):
    """
    Collect all US-Movies from given year

    Args:
         year (str): Year from which to collect movie titles

     Return:
         movie_titles (List) : List of movies in that year with their wikipedia name
    """

    # Scrap html info

    page_object = wikipedia.page(f"List of American films of {year}", auto_suggest=False)

    page_html = page_object.html()

    # Create soup object
    soup = BeautifulSoup(page_html, "html.parser")

    # Get tables
    tables = soup.find_all('table', {'class': 'wikitable sortable'})

    movie_titles = []

    def util_func(row):  # Getting title help function with except for movies without wikipedia page
        try:
            if len(row.find_all("td")) > 4:
                title = row.find_all("td")[1].find("a").get("title")

                return title
            elif len(row.find_all("td")) == 4:
                title = row.find_all("td")[0].find(
                    "a").get("title")

                return title
            else:
                pass
        except AttributeError:
            pass
        except IndexError:
            pass
    for table in tables:  # Iterate over quartals

        rows = table.find_all('tr')

        movie_titles_quart = [util_func(row) for row in rows]  # Extract movie titles from rows

        movie_titles_quart = [title for title in movie_titles_quart if title is not None]  # Remove None values

        movie_titles += movie_titles_quart

    return movie_titles


def get_imdb_url(pagename):
    """
    Get IMDB-URL from wikipedia page in the External Links section

    Args:
         pagename (str): Name of wikipedia page of movie
    Return:
          imdb_url (str) : IMDB-URL of movie
    """
    # Scrap html info
    page_object = wikipedia.page(pagename, auto_suggest=False)

    page_html = page_object.html()

    # Create soup object
    soup = BeautifulSoup(page_html, "html.parser")

    sections = soup.find_all(title="IMDb")  #all IMDB sections

    for x in sections:
        try:
            if x.previous_element.strip() == "at":
                url = x.previous_element.previous_sibling.get("href")
                imdb_url = url
                break
        except:
             pass
    """    
    external_links_section = soup.find(id="External_links")
    external_links_list = external_links_section.find_next("ul")
    if len(external_links_list) == 8:
        external_links_list = external_links_section.find_next("ul").find_next("ul").find_next("ul")

        # Find the <a> elements within the <ul> element
        links = external_links_list.find_all("a")

        # Iterate over the <a> elements and extract the IMDb URL
        imdb_url = None
        for link in links:
            href = link.get("href")
            if href.startswith("https://www.imdb.com"):
                imdb_url = href
                break
    else:
        external_links_list = external_links_section.find_next("ul")

        # Find the <a> elements within the <ul> element
        links = external_links_list.find_all("a")

        # Iterate over the <a> elements and extract the IMDb URL
        imdb_url = None
        for link in links:
            href = link.get("href")
            if href.startswith("https://www.imdb.com"):
                imdb_url = href
                break
    """

    return imdb_url


def get_wiki_moviedata(pagename):
    """
    Collect different attributes from wikipedia page of movie and corresponding imdb page

    Args:
        pagename (str): Name of wikipedia page of movie
    Return:
        data (dict): Data of movie as a dictionary
    """

    # Scrap html info

    page_object = wikipedia.page(pagename, auto_suggest=False)

    page_html = page_object.html()

    # Create soup object
    soup = BeautifulSoup(page_html, "html.parser")

    # Select information box

    infobox = soup.find("table", {"class": "infobox vevent"})

    # Collect needed information

    data = {}
    #Extra request for title
    name_url = f"https://en.wikipedia.org/wiki/{pagename}"
    response = requests.get(name_url)
    html_content = response.content

    soup_name = BeautifulSoup(html_content, "html.parser")


    data["Title"] = soup_name.find(id="firstHeading").i.get_text()
    # Running time
    try:
        info_data = infobox.find("th", string="Running time").find_next_sibling("td")

        if isinstance(info_data.contents[0], Tag):
            data["Running time"] = info_data.contents[0].contents[0]
        elif isinstance(info_data.contents[0], NavigableString):
            data["Running time"] = info_data.contents[0]
        else:
            data["Running time"] = None
    except AttributeError:
        data["Running time"] = None

    except IndexError:
        info_data = infobox.find("th", string="Running time").find_next_sibling("td").find_next("li")
        data["Running time"] = info_data.contents[0]

    # Country

    # info_data = infobox.find("th", string="Country").find_next_sibling("td")
    # if isinstance(info_data.contents[0], Tag):
    # data["Country"] = info_data.contents[0].contents[0]
    # elif isinstance(info_data.contents[0], NavigableString):
    # data["Country"] = info_data.contents[0]
    # else:
    # data["Country"] = None

    # Budget

    try:
        info_data = infobox.find("th", string="Budget").find_next_sibling("td")
        if isinstance(info_data.contents[0], Tag):  # Hyperref case
            data["Budget"] = info_data.contents[0].contents[0]
        elif isinstance(info_data.contents[0], NavigableString):
            data["Budget"] = info_data.contents[0]
        else:
            data["Budget"] = None
    except AttributeError:
        data["Budget"] = None
    except IndexError:
        info_data = infobox.find("th", string="Budget").find_next_sibling("td")
        data["Budget"] =  info_data.contents[1].find('li').text

    # Distribution company

    try:
        info_data = infobox.find("th", string="Distributed by").find_next_sibling("td")
        if isinstance(info_data.contents[0], Tag):  # Case where info has hyperref
            if len(info_data.contents) == 1:
                data["Distribution company"] = info_data.contents[0].contents[0]
            else:
                data["Distribution company"] = info_data.contents[1].find('li').text
        elif isinstance(info_data.contents[0], NavigableString):  # Case where info does not have hyperref
            data["Distribution company"] = info_data.contents[0]
        else:
            data["Distribution company"] = None

    except AttributeError:
        data["Distribution company"] = None

    # Release Date month

    release_date_row = infobox.find('th', string=['Release date', 'Release dates'])
    try:
        if release_date_row.string == "Release dates":  # Multiple dates
            info_data = infobox.find("th", string="Release dates").find_next_sibling("td")
            info = info_data.contents[1].find_all('li')[-1].get_text().split('(')[0].strip()
            try:
                release_date = datetime.datetime.strptime(info, '%B %d, %Y')  # Date Format %B %d %Y
                data["Release month"] = release_date.strftime('%B')
            except ValueError:
                date_obj = datetime.datetime.strptime(info, "%d %B %Y")  # Date Format %d %B %Y
                data["Release month"] = date_obj.strftime("%B")

        else:
            info_data = infobox.find("th", string="Release date").find_next_sibling("td")  # Single dates
            info = info_data.contents[1].find_all('li')[-1].get_text().split('(')[0].strip()
            try:
                release_date = datetime.datetime.strptime(info, '%B %d, %Y')  # Date Format %B %d %Y
                data["Release month"] = release_date.strftime('%B')
            except ValueError:
                date_obj = datetime.datetime.strptime(info, "%d %B %Y")  # Date Format %d %B %Y
                data["Release month"] = date_obj.strftime("%B")
    except IndexError:  #Multiple rows ?
        info_data = infobox.find("th", string="Release date").find_next_sibling("td")
        info = info_data.contents[0].get_text().split('(')[0].strip()
        try:
            release_date = datetime.datetime.strptime(info, '%B %d, %Y')  # Date Format %B %d %Y
            data["Release month"] = release_date.strftime('%B')
        except ValueError:
            date_obj = datetime.datetime.strptime(info, "%d %B %Y")  # Date Format %d %B %Y
            data["Release month"] = date_obj.strftime("%B")

    except AttributeError:  #Handle miscalenous movies
            data["Release month"] = None

    except ValueError:    #Handle that countr has own tag
        info = info_data.contents[1].find_all('li')[-2].get_text().split('(')[0].strip()
        try:
            release_date = datetime.datetime.strptime(info, '%B %d, %Y')  # Date Format %B %d %Y
            data["Release month"] = release_date.strftime('%B')
        except ValueError:
            date_obj = datetime.datetime.strptime(info, "%d %B %Y")  # Date Format %d %B %Y
            data["Release month"] = date_obj.strftime("%B")
    # data["Release month"] = info_data.contents[1].find('li').text.strip().split()[0])

    ##Box Office

    try:
        info_data = infobox.find("th", string="Box office").find_next_sibling("td")
        if isinstance(info_data.contents[0], Tag):
            data["Box office"] = info_data.contents[0].contents[0]
        elif isinstance(info_data.contents[0], NavigableString):
            data["Box office"] = info_data.contents[0]
        else:
            data["Box office"] = None
    except:
        data["Box office"] = None

    # Get imdb url
    imdb_url = get_imdb_url(pagename)

    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"}
    response = requests.get(imdb_url, headers=headers)
    page = response.text
    soup = BeautifulSoup(page, "html.parser")

    jsonData = soup.find('script', {"type": "application/ld+json"})

    jsonSourceObj = json.loads(jsonData.string)
    try:
        # Genre
        data["Genres"] = jsonSourceObj["genre"]
    except:
        data["Genres"] = None

    try:
       # Age Rating
        data["Age Rating"] = jsonSourceObj["contentRating"]
    except:
        data["Age Rating"] = None


    return data











