// The deployment artifact is an explicit allowlist, not the repository root.
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "dist");
const files = [
  ["public/index.html", "index.html"],
  ["public/style.css", "style.css"],
  ["public/app.js", "app.js"],
  ["projects.json", "projects.json"],
  ["public/assets/scrna-dashboard.png", "assets/scrna-dashboard.png"],
  ["public/assets/mirror-home.png", "assets/mirror-home.png"],
  ["public/assets/timebox-timer-v2.png", "assets/timebox-timer-v2.png"],
  [
    "../output/pdf/陈思翰_AdventureX_个人作品集.pdf",
    "output/pdf/陈思翰_AdventureX_个人作品集.pdf",
  ],
  [
    "../output/pdf/陈思翰_AdventureX_个人简历.pdf",
    "output/pdf/陈思翰_AdventureX_个人简历.pdf",
  ],
  [
    "../output/pdf/陈思翰_AdventureX_正式简历.pdf",
    "output/pdf/陈思翰_AdventureX_正式简历.pdf",
  ],
];
fs.rmSync(out, { recursive: true, force: true });
for (const [source, dest] of files) {
  const target = path.join(out, dest);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(path.join(__dirname, source), target);
}
console.log(`Built ${files.length} public files to dist/`);
