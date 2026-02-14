import requests
import os

def download_file(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

if __name__ == "__main__":
    os.makedirs('FOTOS/Dynarex', exist_ok=True)
    
    # Zinc Oxide
    download_file(
        "https://cdn-881a96c5-a77b871b.commercebuild.com/e5679379b58995ada200c19806353331/contents/1192/1192_zinc_oxide_ointment_jar_content_FRONTview.png", 
        "FOTOS/Dynarex/ZincOxide.png"
    )
    
    # Neomycin
    download_file(
        "https://m.media-amazon.com/images/I/51wXh0Z9W5L._AC_SX679_.jpg", 
        "FOTOS/Dynarex/Neomycin.jpg"
    )
    
    # Bacitracin (Attempting simpler source or commercebuild if possible, but I don't have a verified one, trying the one from subagent output log earlier even if 404 likely)
    # The subagent list showed: https://cdn-881a96c5-a77b871b.commercebuild.com/e5679379b58995ada200c19806353331/contents/1173/1173_bacitracin_zinc_ointment_tube_on_white.png
    download_file(
        "https://cdn-881a96c5-a77b871b.commercebuild.com/e5679379b58995ada200c19806353331/contents/1173/1173_bacitracin_zinc_ointment_tube_on_white.png", 
        "FOTOS/Dynarex/Bacitracin.png"
    )
