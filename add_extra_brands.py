import re
import json

FILE_PATH = 'products.js'

new_products = [
    # Staxi Healthcare
    {
        "category": "furniture",
        "brand": "Staxi Healthcare",
        "title": "Ally Chair AL010",
        "price": 0.00,
        "desc": "The Ally Chair by Staxi Healthcare provides safe and comfortable patient transport.",
        "specs": ["Model: AL010", "Durable construction", "Patient safety features"],
        "img": "FOTOS/Ally Chair AL010.png"
    },
    {
        "category": "furniture",
        "brand": "Staxi Healthcare",
        "title": "Max Chair ST310",
        "price": 0.00,
        "desc": "Staxi Max Chair ST310, designed for bariatric transport with enhanced capacity.",
        "specs": ["Model: ST310", "High weight capacity", "Ergonomic design"],
        "img": "FOTOS/Max Chair ST310.png"
    },
    {
        "category": "furniture",
        "brand": "Staxi Healthcare",
        "title": "MR Chair MR010",
        "price": 0.00,
        "desc": "MR Chair MR010 active transport wheelchair by Staxi.",
        "specs": ["Model: MR010", "MRI Compatible options available (check specs)", "Easy maneuverability"],
        "img": "FOTOS/MR Chair MR010.png"
    },
    {
        "category": "furniture",
        "brand": "Staxi Healthcare",
        "title": "Ranger Chair RA010",
        "price": 0.00,
        "desc": "Ranger Chair RA010, rugged and reliable for various healthcare environments.",
        "specs": ["Model: RA010", "All-terrain capability", "Durable frame"],
        "img": "FOTOS/Ranger Chair RA010.png"
    },
    # Silhouet-Tone
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Soli-Lite",
        "price": 0.00,
        "desc": "Soli-Lite LED photobiomodulation system for advanced aesthetic treatments.",
        "specs": ["LED Technology", "Multiple wavelengths", "Non-invasive"],
        "img": "FOTOS/Soli-Lite.png"
    },
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Spirit",
        "price": 0.00,
        "desc": "Spirit permanent hair removal system.",
        "specs": ["Fast and comfortable", "Effective for all hair types", "Advanced technology"],
        "img": "FOTOS/Spirit.png"
    },
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Ultrafraxel CO2 Laser",
        "price": 0.00,
        "desc": "Ultrafraxel CO2 Laser for skin resurfacing and rejuvenation.",
        "specs": ["CO2 Fractional Laser", "Precise control", "Anti-aging solution"],
        "img": "FOTOS/ULTRAFRAXEL CO2 LASER.png"
    },
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Elite Silver Star",
        "price": 0.00,
        "desc": "Elite Silver Star advanced aesthetic device.",
        "specs": ["Professional grade", "Multi-functional", "High performance"],
        "img": "FOTOS/ELITE SILVER STAR.png"
    },
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Elite Bronze",
        "price": 0.00,
        "desc": "Elite Bronze specialized treatment system.",
        "specs": ["Ergonomic design", "Reliable results", "User specific settings"],
        "img": "FOTOS/Elite Bronze.png"
    },
    {
        "category": "aesthetic",
        "brand": "Silhouet-Tone",
        "title": "Evolution XHD",
        "price": 0.00,
        "desc": "Evolution XHD electrolysis system.",
        "specs": ["Apilus technology", "High frequency", "Comfortable treatments"],
        "img": "FOTOS/EVOLUTION XHD.png"
    },
    # ZCS International
    {
        "category": "furniture", 
        "brand": "ZCS International",
        "title": "Scrub Serve",
        "price": 0.00,
        "desc": "Automated scrub distribution and management system.",
        "specs": ["Automated dispensing", "RFID tracking", "Inventory management"],
        "img": "FOTOS/SCRUB SERVE.png"
    }
]

print(f"Reading {FILE_PATH}...")
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the highest ID
# Simple regex to find "id": 123
ids = re.findall(r'["\']?id["\']?:\s*(\d+)', content)
max_id = 0
if ids:
    max_id = max(map(int, ids))

print(f"Max ID found: {max_id}")
current_id = max_id + 1

# Prepare new entries string
new_entries_str = []
for p in new_products:
    p['id'] = current_id
    current_id += 1
    
    # Format as valid JS object (keys can be unquoted if simple, but we'll use quotes for safety or matching style)
    # The file has mixed style now maybe? Let's use clean indentation.
    entry = "    {\n"
    entry += f"        id: {p['id']},\n"
    entry += f"        category: '{p['category']}',\n"
    entry += f"        brand: '{p['brand']}',\n"
    entry += f"        title: '{p['title']}',\n"
    entry += f"        price: {p['price']},\n"
    entry += f"        desc: '{p['desc']}',\n"
    # Specs array
    specs_str = ", ".join([f"'{s}'" for s in p['specs']])
    entry += f"        specs: [{specs_str}],\n"
    entry += f"        img: '{p['img']}'\n"
    entry += "    }"
    new_entries_str.append(entry)

blob = ",\n".join(new_entries_str)

# Insert before the closing bracket
# Assuming end of file is like ... ];
# We find the last bracket
last_bracket_index = content.rfind(']')

if last_bracket_index != -1:
    # Check if we need a comma for the previous item
    # Look at chars before bracket
    pre_content = content[:last_bracket_index].rstrip()
    if not pre_content.endswith(','):
        blob = ",\n" + blob
    else:
        blob = "\n" + blob # Just newline
        
    final_content = content[:last_bracket_index] + blob + "\n" + content[last_bracket_index:]
    
    print("Writing updated content...")
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("Success.")
else:
    print("Could not find closing bracket array in products.js")
