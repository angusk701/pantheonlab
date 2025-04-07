import requests
import hmac
import hashlib
from datetime import datetime, timezone
import base64
import json
import time
import asyncio
from asyncio import Task

from api_keys import storyblocks_pubkey, storyblocks_privkey, unsplash_key, pixabay_key

search_term = input()

async def fetch_unsplash(session, search_term):
    ### This is for unsplash
    url = f"https://api.unsplash.com/photos?query={search_term}"

    response = requests.get(url, headers={'Authorization': f'Client-ID {unsplash_key}'})

    #Check if the request was successful
    if response.status_code == 200:
        response_json = response.json()
        # print(response_json)
        # Extract the required elements
        extracted_data_unsplash = []
        for photo in response_json:
            extracted_data_unsplash.append({
                'image_ID': photo['id'],
                'thumbnails': photo['urls']['thumb'],
                'preview': photo['urls']['small'],  # Assuming preview is the same as small
                'title': photo.get('alt_description', 'No title available'),
                'source': 'Unsplash',
                'tags': []  # Unsplash does not provide tags in the search response
            })
        
        # print(extracted_data_unsplash)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

### This is for pixabay
# encode search term before passing into url

search_term_pix = search_term.replace(" ","+")
print(search_term_pix)

url_pix = f"https://pixabay.com/api/?key={pixabay_key}&q={search_term_pix}"
response_pix = requests.get(url_pix)

if response.status_code == 200:
    response_pix_json = response_pix.json()
    
    # Extract the required elements
    extracted_data_pixabay = []

    for hit in response_pix_json['hits']:
        extracted_data_pixabay.append({
            'image_ID': hit['id'],
            'thumbnails': hit['previewURL'],
            'preview': hit['webformatURL'],  # Assuming preview is the same as webformat
            'title': None,  # Pixabay does not provide a title
            'source': 'Pixabay',
            'tags': hit['tags'].split(',')  # Split tags into an array
        })
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

## This is for storyblocks
# hmac generation
baseUrl = "https://api.graphicstock.com"
resource = "/api/v2/images/search"
expires = str(int(time.time()) + 120)
hmacBuilder = hmac.new(bytearray(storyblocks_privkey + expires, 'utf-8'), resource.encode('utf-8'), hashlib.sha256)
hmacHex = hmacBuilder.hexdigest()

url_sb = f"https://api.graphicstock.com/api/v2/images/search?APIKEY={storyblocks_pubkey}&EXPIRES={expires}&HMAC={hmacHex}&keywords={search_term}"

response_sb = requests.get(url_sb)

if response_sb.status_code == 200:
    response_sb_json = response_sb.json()

    print(response_sb_json)
else:
    print(f"Failed to retrieve data. Status code: {response_sb.status_code}")


# async def fetch_status(url:str) -> dict:
#     print(f'Fetching status for: {url}')
#     response = await asyncio.to_thread(requests.get, url, None)
#     print('Done')
#     return {'status': response.status_code, 'url': url}

# async def main() -> None:

# if __name__ == '__main__':
#     asyncio.run(main=main())