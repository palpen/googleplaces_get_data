"""
This script takes a string containing restaurant name and address and returns info
on rating and price level using the Google Places Search API

Google Places Search API documentation
- https://developers.google.com/places/web-service/search

Data to pull
1. Name
2. Price
3. Url
4. rating
5. total number of reviews (if they have it)
"""

import io
import json
import requests
import pandas as pd
import re
import csv
import numpy as np


def prepare_search_query(restaurant_list, restaurant_id_col='uid_rest_gl', restaurant_name_col='location_name'):

    df = pd.read_csv(restaurant_list, encoding='ISO-8859-1')

    # strip front and back space
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    # dataframe of only object types (i.e. strings)
    df_obj = df.select_dtypes(include=['object'])

    # list containing column names of only object types (e.g. strings)
    obj_cols = list(df_obj.columns)
    print(obj_cols)

    # for location name with forward slash in name, keep only restaurant
    # name before the forward slash
    df[restaurant_name_col] = df[restaurant_name_col].apply(lambda x: x.split('/')[0])

    # remove and non-alphanumeric characters
    # and combine strings into one column
    df['search_query'] = ""

    for col in obj_cols:
        df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))
        df['search_query'] = df['search_query'] + " " + df[col]

    # strip front and back whitespace again
    df['search_query'] = df['search_query'].apply(lambda x: x.strip())

    # make everything lower case
    df['search_query'] = df['search_query'].str.lower()

    # remove double spaces
    df['search_query'] = df['search_query'].apply(lambda x: re.sub(r"\s\s+", " ", x))

    return df[[restaurant_id_col, 'search_query']]


def make_http_url(textsearch, api_key):
    return "https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&key={1}".format(textsearch, api_key)


def is_key_in_json(key, json):
    if key in json:
        return json[key]
    return np.NaN


if __name__ == '__main__':

    ################################################################################
    # Palermo's path
    PATH = "/Users/palermospenano/Desktop/Dropbox/temporary/limin_py/googleplaces_get_data/"
    in_csv = "unique_restaurants_for_Google.csv"

    in_start = 60
    in_end = 63
    out_csv = "{2}data/gp_start{0}_end{1}.csv".format(in_start, in_end, PATH)
    ################################################################################

    # read API keys
    with io.open('credentials.json') as cred:
        creds = json.load(cred)
        api_key = creds['api_key']

    df_sq = prepare_search_query(f'{PATH}data/{in_csv}', restaurant_id_col='uid_rest_gl', restaurant_name_col='location_name')

    header = ['uid', 'search_query', 'name', 'result_address', 'rating', 'price_level']

    with open(out_csv, 'w') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(header)

        # use in_start and in_end to restrict script running to these values
        ids = df_sq['uid_rest_gl'].loc[in_start:in_end]
        queries = df_sq['search_query'].loc[in_start:in_end]

        count = in_start

        for i, q in zip(ids, queries):

            print("Count:", count)
            print(q)
            get = requests.get(make_http_url(q, api_key))
            results = get.json()['results']

            for r in results:

                name = is_key_in_json('name', r)
                result_address = is_key_in_json('formatted_address', r)
                rating = is_key_in_json('rating', r)
                price_level = is_key_in_json('price_level', r)

                data = [i, q, name, result_address, rating, price_level]

                writer.writerow(data)

            print("=" * 20)
            print("")

            count += 1
