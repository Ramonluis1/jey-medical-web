const fs = require('fs');

try {
    // Read products.js directly and wrap it
    const content = fs.readFileSync('products.js', 'utf8');
    if (!content.includes('module.exports')) {
        fs.writeFileSync('temp_products_verify_v2.js', content + '\nmodule.exports = products;');
    } else {
        fs.writeFileSync('temp_products_verify_v2.js', content);
    }

    const currentProducts = require('./temp_products_verify_v2.js');

    let logoCount = 0;
    let dynarexUrlCount = 0;
    let zCount = 0;

    currentProducts.forEach(p => {
        if (p.img) {
            if (p.img.includes('logo.png')) logoCount++;
            if (p.img.includes('dynarex.com/media')) dynarexUrlCount++;
            if (p.img.startsWith('z-') || p.img.includes('/z-')) zCount++;
        }
    });

    console.log(`Verification Report:`);
    console.log(`- Products still using logo.png: ${logoCount}`);
    console.log(`- Products now using Dynarex URLs: ${dynarexUrlCount}`);
    console.log(`- Products using z- placeholders (left untouched): ${zCount}`);

    // Clean up
    try { fs.unlinkSync('temp_products_verify_v2.js'); } catch (e) { }

} catch (e) {
    console.error(e);
}
