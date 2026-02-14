const fs = require('fs');

try {
    // 1. Load the current 'bad' products
    const content = fs.readFileSync('products.js', 'utf8');
    if (!content.includes('module.exports')) {
        fs.writeFileSync('temp_products_revert.js', content + '\nmodule.exports = products;');
    } else {
        fs.writeFileSync('temp_products_revert.js', content);
    }
    const currentProducts = require('./temp_products_revert.js');

    // 2. Load the original data for missing photos from the report
    // This report was generated BEFORE the fix, so it has the original 'z-' paths.
    if (!fs.existsSync('report_missing.json')) {
        console.error("Critical: report_missing.json not found! Cannot automatically revert.");
        process.exit(1);
    }
    const originalData = JSON.parse(fs.readFileSync('report_missing.json', 'utf8'));

    // Create a map for fast lookup
    const originalMap = {};
    originalData.forEach(item => {
        originalMap[item.id] = item.img;
    });

    let revertedCount = 0;

    // 3. Revert
    const revertedProducts = currentProducts.map(p => {
        if (originalMap[p.id]) {
            // Restore original image
            p.img = originalMap[p.id];
            revertedCount++;
        }
        return p;
    });

    console.log(`Reverted ${revertedCount} products to their original state.`);

    // 4. Save
    const fileContent = `const products = ${JSON.stringify(revertedProducts, null, 4)};`;
    fs.writeFileSync('products.js', fileContent);
    console.log('Successfully restored products.js using report_missing.json');

    // Clean up
    try { fs.unlinkSync('temp_products_revert.js'); } catch (e) { }

} catch (err) {
    console.error("Error reverting:", err);
}
