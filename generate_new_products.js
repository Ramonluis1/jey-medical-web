
const fs = require('fs');
const path = require('path');

const photoDir = 'FOTOS/Dynarex';
const startId = 4783;

// Known brands to exclude
const excluded = new Set([
    'LabChoice.png', 'CodeBlueCare.png', 'DynaSafety.png', 'WeCare.png',
    'DynaCare.png', 'Resp-O2.png', 'Glenshaw.png', 'BariMax.png',
    'Durma.png', 'CurPro.png', 'Ridgewood.png', 'Montclair.png',
    'DispoSafetyBrand.png', 'SafeTouch.png', 'DMECare.png', 'Fearless.png',
    'logo.png', 'd-logo.png', 'dynarex-logo.png'
]);

// Read products.js to find used images
const prodFile = fs.readFileSync('products.js', 'utf8');
const used = new Set();
// Simple regex to catch "img": "..."
let match;
const re = /"img":\s*"([^"]+)"/g;
while ((match = re.exec(prodFile)) !== null) {
    used.add(path.basename(match[1]).toLowerCase());
}

if (fs.existsSync(photoDir)) {
    const files = fs.readdirSync(photoDir).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f));
    let id = startId;
    const newProds = [];

    files.forEach(f => {
        if (excluded.has(f)) return;
        if (used.has(f.toLowerCase())) return;

        // Determine category and title
        let cat = 'General Supplies';
        let brand = 'Dynarex';

        // Clean up title
        let name = path.parse(f).name;
        let title = name.replace(/^z-/, '').replace(/-/g, ' ');

        // Logic
        const nameLower = f.toLowerCase();

        // Gloves
        if (/^\d{4}-BX/.test(f) || /^\d{4}-EA/.test(f) || /glove/i.test(nameLower) || ['2336', '2337', '2360', '2616', '3040'].some(s => nameLower.includes(s))) {
            cat = 'Gloves';
            if (!/glove/i.test(title)) title = `Latex/Nitrile Gloves ${title}`;
        }
        // Furniture / Mobility (125xx series are usually Recliners)
        else if (nameLower.startsWith('125') || /chair|recliner|bed|rail|stool/i.test(nameLower)) {
            cat = 'Mobility & Furniture';
            if (!/chair|recliner|bed/i.test(title)) title = `Medical Furniture ${title}`;
        }
        // Ointments
        else if (/ointment|cream|zinc|freeze/i.test(nameLower)) {
            cat = 'Ointments & Creams';
        }
        // Respiratory/Masks
        else if (/mask|respiratory|oxygen/i.test(nameLower)) {
            cat = 'Apparel'; // Or respiratory
            if (/mask/i.test(nameLower)) cat = 'Gowns & Apparel';
        }

        newProds.push({
            id: id++,
            category: cat,
            brand: brand,
            title: title + (name.startsWith('z-') ? '' : ` (SKU: ${name})`),
            price: 0,
            desc: `High quality ${title}.`,
            specs: ["Manufacturer: Dynarex", `SKU: ${name}`, "Professional Grade"],
            img: `FOTOS/Dynarex/${f}`
        });
    });

    fs.writeFileSync('new_products.json', JSON.stringify(newProds, null, 4), 'utf8');
    console.log("Wrote " + newProds.length + " new products to new_products.json");
}
