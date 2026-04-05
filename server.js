const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const PUBLIC = path.join(__dirname, 'public');

const MIME = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.json': 'application/json', '.ico': 'image/x-icon',
};

// Clean URL → file path mappings
const ROUTES = {
  '/':             '/index.html',
  '/certificate':  '/certificate.html',
  '/start':        '/index.html',
};

http.createServer((req, res) => {
  let urlPath = req.url.split('?')[0];

  // Named routes
  if (ROUTES[urlPath]) urlPath = ROUTES[urlPath];

  // /stop/N → /stops/stopN.html
  const stopMatch = urlPath.match(/^\/stop\/(\d+)$/);
  if (stopMatch) urlPath = `/stops/stop${stopMatch[1]}.html`;

  const filePath = path.join(PUBLIC, urlPath);
  const ext = path.extname(filePath);
  const contentType = MIME[ext] || 'text/plain';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1 style="font-family:monospace;color:#00d4c8;background:#050a14;padding:40px">404 — Atlas signal lost</h1>');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType + '; charset=utf-8' });
    res.end(data);
  });
}).listen(PORT, '0.0.0.0', () => {
  console.log(`NMS Easter Quest running on http://0.0.0.0:${PORT}`);
  console.log(`  /              -> Start page`);
  console.log(`  /stop/1-10     -> Waypoints`);
  console.log(`  /certificate   -> Certificate`);
});
