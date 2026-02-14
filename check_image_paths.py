
import os
import re
import difflib

PRODUCTS_FILE = 'products.js'
HTML_FILE = 'index.html'
FOTOS_DIR = 'FOTOS'

def normalize_path(path):
    return path.replace('\\', '/')

def find_best_match(target, candidates):
    # exact match case insensitive
    target_lower = target.lower()
    for c in candidates:
        if c.lower() == target_lower:
            return c
    # fuzzy match
    matches = difflib.get_close_matches(target, candidates, n=1, cutoff=0.8)
    if matches:
        return matches[0]
    return None

def main():
    with open('report.txt', 'w', encoding='utf-8') as f:
        f.write("Checking image paths...\n")
        
        # 1. Load all files in FOTOS recursively
        actual_files = []
        for root, dirs, files in os.walk(FOTOS_DIR):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                actual_files.append(normalize_path(rel_path))
        
        f.write(f"Found {len(actual_files)} files in {FOTOS_DIR}\n")

        # 2. Parse products.js
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as pf:
            content = pf.read()
        
        # Extract img: 'PATH' or "img": "PATH"
        product_images = re.findall(r'["\']?img["\']?\s*:\s*["\'](.+?)["\']', content)
        
        broken_products = []
        
        f.write(f"\nChecking {len(product_images)} product images...\n")
        
        external_urls = []
        for img_path in product_images:
            if img_path.startswith('http'):
                external_urls.append(img_path)
                continue
                
            norm_path = normalize_path(img_path)
            if norm_path not in actual_files:
                match = find_best_match(norm_path, actual_files)
                broken_products.append((img_path, match))
        
        f.write(f"\nFound {len(external_urls)} external URLs among product images.\n")
        
        # Check sample of external URLs
        import urllib.request
        import urllib.error
        
        if external_urls:
            f.write("\nChecking sample of 5 external URLs:\n")
            for url in external_urls[:5]:
                try:
                    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=5) as response:
                        f.write(f"  [OK] {url[:60]}... status {response.status}\n")
                except Exception as e:
                    f.write(f"  [FAIL] {url[:60]}... error {e}\n")


        # 3. Parse brandLogos from index.html
        with open(HTML_FILE, 'r', encoding='utf-8') as hf:
            html_content = hf.read()
        
        brand_logos_match = re.search(r'const brandLogos = \{([^}]+)\}', html_content, re.DOTALL)
        broken_brands = []
        if brand_logos_match:
            block = brand_logos_match.group(1)
            brand_images = re.findall(r':\s*["\'](.+?)["\']', block)
            f.write(f"\nChecking {len(brand_images)} brand logos...\n")
            for img_path in brand_images:
                if img_path.startswith('http'): 
                    continue
                
                check_path = normalize_path(img_path)
                if not check_path.startswith('FOTOS/'):
                    check_path_with_prefix = f"FOTOS/{check_path}"
                else:
                    check_path_with_prefix = check_path
                    
                if check_path_with_prefix not in actual_files:
                     match = find_best_match(check_path_with_prefix, actual_files)
                     broken_brands.append((img_path, match))
        else:
            f.write("\nCould not find 'const brandLogos' object in HTML.\n")

        # Report
        f.write("-" * 40 + "\n")
        f.write("RESULTS\n")
        f.write("-" * 40 + "\n")
        
        if broken_products:
            f.write(f"\nFound {len(broken_products)} broken product images:\n")
            for original, suggestion in broken_products:
                f.write(f"  Broken: {original}\n")
                if suggestion:
                    f.write(f"  Suggest: {suggestion}\n")
                else:
                    f.write("  No match found.\n")
        else:
            f.write("\nNo broken product images found (local files).\n")

        if broken_brands:
            f.write(f"\nFound {len(broken_brands)} broken brand logos:\n")
            for original, suggestion in broken_brands:
                f.write(f"  Broken: {original}\n")
                if suggestion:
                    f.write(f"  Suggest: {suggestion}\n")
                else:
                    f.write("  No match found.\n")
        else:
            f.write("\nNo broken brand logos found.\n")

    print("Done. Wrote report.txt")

if __name__ == '__main__':
    main()
