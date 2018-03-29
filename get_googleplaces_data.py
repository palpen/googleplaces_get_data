"""
Google Places Search API documentation
- https://developers.google.com/places/web-service/search

Data to pull
1. Name
2. Price
3. Url
4. rating
5. total number of reviews (if they have it)

To do:
- code to clean up text file (in separate utils.py)
- code to write results to csv file
"""

import io
import json
import requests

import pprint as pp


def make_http_url(textsearch, api_key):
    return "https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&key={1}".format(textsearch, api_key)


if __name__ == '__main__':

    # read API keys
    with io.open('credentials.json') as cred:
        creds = json.load(cred)
        api_key = creds['api_key']

    # search_query = 'PINE STREET GRILL 505 Pine St Abilene TX 79601 USA'
    search_query = 'CHILIS GRILL BAR 210 E Commerce St Brownwood TX 76801 USA'

    get = requests.get(make_http_url(search_query, api_key))

    results = get.json()['results']
    pp.pprint(results)

    for r in results:
        print("")
        print("")

        print("Name:", r['name'])
        print("Address:", r['formatted_address'])

        try:
            print("Rating:", r['rating'])
        except:
            print("No rating")
        try:
            print("Price:", r['price_level'])
        except:
            print("No price")
