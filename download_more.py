import requests
import os

def download_file(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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
    # Neomycin from Express Medical Supply
    download_file(
        "https://www.expressmedicalsupply.com/media/catalog/product/D/Y/DYN1163_1.jpg", 
        "FOTOS/Dynarex/Neomycin.jpg"
    )
    
    # Bacitracin - trying a new guessed/searched link or McKesson alternate
    # 2113.jpg exists in the folder, might be related?
    # Trying another common medical supply site pattern or just a google image result if I had one
    # I'll try one found in logs: https://www.vitalitymedical.com/dynarex-neomycin-ointment.html -> image?
    # Let's try to get Bacitracin from a different source if possible.
    # Trying a generic one:
    # https://medicomart.com/wp-content/uploads/2020/05/1173.jpg (Guessing based on SKU 1173)
    
    download_file(
        "https://www.expressmedicalsupply.com/media/catalog/product/D/Y/DYN1173_1.jpg",
        "FOTOS/Dynarex/Bacitracin.jpg"
    )
