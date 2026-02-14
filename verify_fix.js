const fs = require('fs');

try {
    const content = fs.readFileSync('products.js', 'utf8');
    if (!content.includes('module.exports')) {
        fs.writeFileSync('temp_products_verify.js', content + '\nmodule.exports = products;');
    } else {
        fs.writeFileSync('temp_products_verify.js', content);
    }
} catch (e) {
    console.error("Error reading products.js", e);
    process.exit(1);
}

const products = require('./temp_products_verify.js');

let zCount = 0;
let dynarexUrlCount = 0;
let invalidCount = 0;

products.forEach(p => {
    if (!p.img) {
        invalidCount++;
        return;
    }

    if (p.img.includes('/z-') || p.img.startsWith('z-')) {
        zCount++;
    }

    if (p.img.includes('dynarex.com/media')) {
        dynarexUrlCount++;
    }
});

console.log(`Remaining z- images: ${zCount}`);
console.log(`Injected Dynarex URLs: ${dynarexUrlCount}`);
console.log(`Total products: ${products.length}`);

// Clean up
try { fs.unlinkSync('temp_products_verify.js'); } catch (e) { }
