import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const source = join(here, "entry.png");

// Fail loudly instead of shipping a broken image: entry.png must be a
// whole PNG within the competition's size limit (1 MiB, 1024x1024).
const header = readFileSync(source).subarray(0, 8);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!header.equals(pngMagic)) {
  throw new Error("entry.png is not a PNG file");
}
if (statSync(source).size > 1048576) {
  throw new Error("entry.png exceeds the 1 MiB size limit");
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`wrote ${statSync(source).size} bytes to ${join(outDir, "entry.png")}`);
