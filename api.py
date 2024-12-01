import requests

# Unsplash API Access Key (replace 'YOUR_ACCESS_KEY' with your actual key)
UNSPLASH_ACCESS_KEY = "DHAUbvogxnfk9WCspr0SuxtPgpnFFJxa-8A6nKMVcoU"

def get_unsplash_image(search_query):
    """
    Fetch an image URL from Unsplash based on the search query.

    :param search_query: The term to search for (e.g., city name).
    :return: A URL to the image or None if not found.
    """
    search_query = search_query + ' houses'
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": search_query,  # Search term
        "client_id": UNSPLASH_ACCESS_KEY,  # Access Key
        "per_page": 1,  # Number of results
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]  # Image URL
        else:
            return None  # No image found
    else:
        raise Exception(f"Error fetching image from Unsplash: {response.status_code}")
