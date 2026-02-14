const fs = require('fs');
const path = require('path');

// 1. Create a temp module to load products
try {
    const content = fs.readFileSync('products.js', 'utf8');
    if (!content.includes('module.exports')) {
        fs.writeFileSync('temp_products_repair_v2.js', content + '\nmodule.exports = products;');
    } else {
        fs.writeFileSync('temp_products_repair_v2.js', content);
    }
} catch (e) {
    console.error("Error reading products.js", e);
    process.exit(1);
}

const products = require('./temp_products_repair_v2.js');

// Helper to check if image is "bad" OR placeholder
function isBadImage(p) {
    // 1. Explicit placeholder or logo
    if (!p.img || p.img.includes('placehold.co') || p.img.includes('Image+Not+Available') || p.img.includes('logo.png')) {
        return true;
    }
    // 2. Local file missing check (safe check)
    if (p.img && !p.img.startsWith('http')) {
        try {
            if (!fs.existsSync(p.img)) return true;
        } catch (e) { return true; }
    }
    return false;
}

// Helper to extract SKU
function getSku(p) {
    let sku = '';
    if (p.specs && p.specs.length) {
        const skuSpec = p.specs.find(s => s.includes('SKU:'));
        if (skuSpec) {
            sku = skuSpec.replace('SKU:', '').trim();
        }
    }
    if (!sku && p.desc) {
        const match = p.desc.match(/SKU:\s*([^)]+)/);
        if (match) sku = match[1];
    }
    return sku;
}

// Helper to construct Dynarex URL
function getDynarexUrl(sku) {
    if (!sku) return null;
    // Basic cleanup for URL construction
    const cleanSku = sku.trim();
    // Logic: media/catalog/product/{char1}/{char2}/{sku}.jpg
    const c1 = cleanSku.charAt(0);
    const c2 = cleanSku.charAt(1);
    return `https://dynarex.com/media/catalog/product/${c1}/${c2}/${cleanSku}.jpg`;
}

let fixedCount = 0;
let skippedZCount = 0;

// Pass: Fix images (CONSERVATIVE)
const newProducts = products.map(p => {
    const isDynarex = p.brand && p.brand.toUpperCase().includes('DYNAREX');

    // Only proceed if it is Dynarex AND image is seemingly bad/missing
    if (isDynarex && isBadImage(p)) {
        const sku = getSku(p);

        // STRICT CHECK: Must have SKU and NOT start with z-
        // Also check if SKU is valid string
        if (sku && !sku.toLowerCase().startsWith('z-') && !sku.toLowerCase().includes('unknown')) {
            const newUrl = getDynarexUrl(sku);
            if (newUrl) {
                // console.log(`Fixing ${sku} with ${newUrl}`);
                p.img = newUrl;
                fixedCount++;
            }
        } else {
            // Count skipped z- items for reporting
            if (sku && sku.toLowerCase().startsWith('z-')) {
                skippedZCount++;
            }
        }
    }
    return p;
});

console.log(`Conservative Repair Summary:`);
console.log(`- Fixed ${fixedCount} products with valid numeric SKUs.`);
console.log(`- Skipped ${skippedZCount} products with internal 'z-' SKUs (left as is).`);

// Convert back to JS file format
const fileContent = `const products = ${JSON.stringify(newProducts, null, 4)};`;

// Write to products.js (overwriting!)
fs.writeFileSync('products.js', fileContent);
console.log('Successfully updated products.js');

// Clean up
try { fs.unlinkSync('temp_products_repair_v2.js'); } catch (e) { }
