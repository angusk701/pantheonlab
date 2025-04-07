import asyncio
import hmac
import hashlib
import time
from urllib.parse import quote_plus
import aiohttp

from api_keys import storyblocks_pubkey, storyblocks_privkey, unsplash_key, pixabay_key


async def fetch_unsplash(session, search_term):
    url = f"https://api.unsplash.com/photos?query={search_term}"
    async with session.get(url, headers={'Authorization': f'Client-ID {unsplash_key}'}) as response:
        if response.status == 200:
            data = await response.json()
            return [{
                'image_ID': photo['id'],
                'thumbnails': photo['urls']['thumb'],
                'preview': photo['urls']['small'],
                'title': photo.get('alt_description', 'No title available'),
                'source': 'Unsplash',
                'tags': []
            } for photo in data]
        return []


async def fetch_pixabay(session, search_term):
    """Fetch data from Pixabay API."""
    encoded_search = quote_plus(search_term)
    url = f"https://pixabay.com/api/?key={pixabay_key}&q={encoded_search}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return [{
                'image_ID': hit['id'],
                'thumbnails': hit['previewURL'],
                'preview': hit['webformatURL'],
                'title': None,
                'source': 'Pixabay',
                'tags': hit['tags'].split(',')
            } for hit in data.get('hits', [])]
        return []


async def fetch_storyblocks(session, search_term):
    """Fetch data from Storyblocks API."""
    base_url = "https://api.graphicstock.com"
    resource = "/api/v2/images/search"
    expires = str(int(time.time()) + 120)

    # Generate HMAC signature
    signing_key = storyblocks_privkey + expires
    hmac_sig = hmac.new(
        signing_key.encode('utf-8'),
        resource.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    url = f"{base_url}{resource}?APIKEY={storyblocks_pubkey}&EXPIRES={expires}&HMAC={hmac_sig}&keywords={quote_plus(search_term)}"

    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            return [{
                'image_ID': item['id'],
                'thumbnails': item['thumbnail_url'],
                'preview': item['preview_url'],
                'title': item.get('title', 'No title available'),
                'source': 'Storyblocks',
                'tags': []
            } for item in data.get('results', [])]
        return []


async def main(search_term):
    async with aiohttp.ClientSession() as session:
        # Fetch data concurrently from all APIs
        unsplash_data, pixabay_data, storyblocks_data = await asyncio.gather(
            fetch_unsplash(session, search_term),
            fetch_pixabay(session, search_term),
            fetch_storyblocks(session, search_term)
        )

        # Combine results from all sources
        combined_results = unsplash_data + pixabay_data + storyblocks_data
        return combined_results


if __name__ == '__main__':
    search_term = input("Enter search term: ")
    results = asyncio.run(main(search_term))
    
    print(f"Total results: {len(results)}")
    for result in results: 
        print(result)