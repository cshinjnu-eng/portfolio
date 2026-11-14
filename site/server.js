// Serve only the generated public artifact, never the repository root.
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "../dist");
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".mp4": "video/mp4",
  ".webm": "video/webm",
  ".pdf": "application/pdf",
};
http
  .createServer((req, res) => {
    if (!["GET", "HEAD"].includes(req.method)) {
      res.writeHead(405, { Allow: "GET, HEAD" });
      return res.end();
    }
    let pathname;
    try {
      pathname = decodeURIComponent(
        new URL(req.url, "http://localhost").pathname,
      );
    } catch {
      res.writeHead(400);
      return res.end();
    }
    if (/[\x00-\x1f\x7f]/.test(pathname)) {
      res.writeHead(400);
      return res.end("Bad request");
    }
    if (pathname.split("/").some((x) => x.startsWith("."))) {
      res.writeHead(404);
      return res.end("Not found");
    }
    if (pathname === "/api/projects") pathname = "/projects.json";
    if (pathname.endsWith("/")) pathname += "index.html";
    const file = path.resolve(root, "." + pathname);
    if (!file.startsWith(root + path.sep)) {
      res.writeHead(404);
      return res.end("Not found");
    }
    fs.readFile(file, (err, data) => {
      if (err) {
        res.writeHead(404);
        return res.end("Not found");
      }
      res.writeHead(200, {
        "Content-Type":
          types[path.extname(file).toLowerCase()] || "application/octet-stream",
        "X-Content-Type-Options": "nosniff",
      });
      res.end(req.method === "HEAD" ? undefined : data);
    });
  })
  .listen(Number(process.env.PORT) || 8766, "127.0.0.1", function () {
    console.log(`Portfolio: http://127.0.0.1:${this.address().port}`);
  });
