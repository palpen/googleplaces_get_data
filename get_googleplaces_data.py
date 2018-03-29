import io
import json



search_query = "test"
HTTP_URL = "https://maps.googleapis.com/maps/api/place/radarsearch/output?parameters"


if __name__ == '__main__':

    # read API keys
    with io.open('credentials.json') as cred:
        creds = json.load(cred)
        api_key = creds['api_key']

