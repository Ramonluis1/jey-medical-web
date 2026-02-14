import requests
import re

def search_image_backup(query):
    # Simple scraper for DDG Lite (HTML version)
    # This is a fallback if the library isn't there.
    # Note: DDG HTML might have bot protection, but it's worth a try for a few items.
    url = "https://duckduckgo.com/html/"
    params = {'q': query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        res = requests.post(url, data=params, headers=headers)
        # Look for image results... finding image results in DDG HTML is tricky because they are mostly web links.
        # But we can try to find the FIRST result link, visit it, and find the largest image? That's too complex.
        
        # Let's try searching for the IMAGE directly?
        # DDG Images requires JS usually.
        
        # Alternative: Search for product PAGE and take the first image on that page?
        # Let's look at the result content.
        if "Laryngeal Mask" in res.text:
             print("Search returned results.")
        else:
             print("Search returned no text match.")
             
        # Just to check if we can even SEARCH.
        print(f"Status: {res.status_code}")
        
    except Exception as e:
        print(f"Error: {e}")

try:
    from duckduckgo_search import DDGS
    print("DDGS Library is available!")
    with DDGS() as ddgs:
        results = list(ddgs.images(
            keywords="Dynarex 36294",
            region="wt-wt",
            safesearch="off",
            size="medium",
            max_results=1
        ))
        if results:
            print(f"Found image: {results[0]['image']}")
        else:
            print("No image found via Library.")
except ImportError:
    print("DDGS Library NOT available. Using backup request...")
    search_image_backup("Dynarex 36294")
