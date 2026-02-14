
const fs = require('fs');
const path = require('path');

// Mock browser environment if needed or just execute the file
// But products.js has `const products = ...`. If we use require/import it might fail if not module.
// So let's read file, eval it in a context.
const productsFile = path.join(__dirname, 'products.js');
const fileContent = fs.readFileSync(productsFile, 'utf8');

// Isolate the array content
// Remove "const products =" and assume the rest is valid JS object/array literal
// We can use eval() in a clean context or just execute it.
// Wait, `products.js` is just data assignment. 
try {
    // Determine start of array
    const start = fileContent.indexOf('[');
    const end = fileContent.lastIndexOf(']');
    if (start === -1 || end === -1) throw new Error("Format not recognized");

    const arrayString = fileContent.substring(start, end + 1);
    // Use Function constructor to safely evaluate array literal
    // This handles comments, trailing commas, unquoted keys if any (though usually JSON keys serve best).
    // Actually `eval` or `new Function` is standard way to parse JS object literals.
    const products = eval(arrayString);

    // Now check files
    const photosDir = path.join(__dirname, 'FOTOS/Dynarex');
    if (!fs.existsSync(photosDir)) {
        console.log("Photos dir not found");
        process.exit(0);
    }

    const existingPhotos = fs.readdirSync(photosDir).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f));
    const usedImages = new Set(products.map(p => p.img ? path.basename(p.img).toLowerCase() : ''));

    const unused = existingPhotos.filter(f => !usedImages.has(f.toLowerCase()));

    console.log(JSON.stringify(unused, null, 2));

} catch (e) {
    console.error("Error parsing:", e.message);
}
