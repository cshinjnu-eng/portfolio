const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const root = path.join(__dirname, "public");
const files = new Map([
  ["/", ["index.html", "text/html; charset=utf-8"]],
  ["/index.html", ["index.html", "text/html; charset=utf-8"]],
  ["/style.css", ["style.css", "text/css; charset=utf-8"]],
  ["/app.js", ["app.js", "text/javascript; charset=utf-8"]],
  ["/assets/scrna-dashboard.png", ["assets/scrna-dashboard.png", "image/png"]],
  ["/assets/mirror-home.png", ["assets/mirror-home.png", "image/png"]],
  [
    "/assets/timebox-timer-v2.png",
    ["assets/timebox-timer-v2.png", "image/png"],
  ],
]);
function sendFile(req, res, filename, contentType) {
  fs.readFile(filename, (error, data) => {
    if (error) {
      res.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      return res.end("Resource unavailable");
    }
    res.writeHead(200, {
      "Content-Type": contentType,
      "X-Content-Type-Options": "nosniff",
    });
    res.end(req.method === "HEAD" ? undefined : data);
  });
}
const server = http.createServer((req, res) => {
  if (!["GET", "HEAD"].includes(req.method)) {
    res.writeHead(405, { Allow: "GET, HEAD" });
    return res.end();
  }
  // Match raw paths exactly, without resolving user-provided paths.
  const pathname = req.url.split("?")[0];
  if (pathname === "/api/projects" || pathname === "/projects.json")
    return sendFile(
      req,
      res,
      path.join(__dirname, "projects.json"),
      "application/json; charset=utf-8",
    );
  const pdfNames = [
    "陈思翰_AdventureX_个人作品集.pdf",
    "陈思翰_AdventureX_个人简历.pdf",
    "陈思翰_AdventureX_正式简历.pdf",
  ];
  const pdf = pdfNames.find(
    (name) =>
      pathname === `/output/pdf/${encodeURIComponent(name)}` ||
      pathname === `/output/pdf/${name}`,
  );
  if (pdf)
    return sendFile(
      req,
      res,
      path.join(__dirname, "..", "output", "pdf", pdf),
      "application/pdf",
    );
  const entry = files.get(pathname);
  if (!entry) {
    res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    return res.end("Not found");
  }
  return sendFile(req, res, path.join(root, entry[0]), entry[1]);
});
server.listen(Number(process.env.PORT) || 8766, "127.0.0.1", () =>
  console.log(`Portfolio: http://127.0.0.1:${server.address().port}`),
);
