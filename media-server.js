const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 10000;
const ROOT = path.join(__dirname, 'media');
const routes = {
  '/story.mp4': { file: 'story.mp4', type: 'video/mp4' },
  '/soundtrack.mp3': { file: 'soundtrack.mp3', type: 'audio/mpeg' },
};

function sendFile(req, res, entry) {
  const filePath = path.join(ROOT, entry.file);
  let stat;
  try { stat = fs.statSync(filePath); } catch (_) {
    res.writeHead(404, { 'Content-Type': 'text/plain', 'Access-Control-Allow-Origin': '*' });
    res.end('Media not available');
    return;
  }
  const range = req.headers.range;
  const common = {
    'Content-Type': entry.type,
    'Accept-Ranges': 'bytes',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'public, max-age=86400, immutable',
  };
  if (!range) {
    res.writeHead(200, { ...common, 'Content-Length': stat.size });
    fs.createReadStream(filePath).pipe(res);
    return;
  }
  const m = /bytes=(\d*)-(\d*)/.exec(range);
  if (!m) { res.writeHead(416); res.end(); return; }
  const start = m[1] ? Number(m[1]) : 0;
  const end = m[2] ? Math.min(Number(m[2]), stat.size - 1) : stat.size - 1;
  if (start > end || start >= stat.size) { res.writeHead(416); res.end(); return; }
  res.writeHead(206, {
    ...common,
    'Content-Range': `bytes ${start}-${end}/${stat.size}`,
    'Content-Length': end - start + 1,
  });
  fs.createReadStream(filePath, { start, end }).pipe(res);
}

http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
    return;
  }
  const entry = routes[req.url];
  if (entry) return sendFile(req, res, entry);
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not found');
}).listen(PORT, '0.0.0.0', () => console.log(`Atlas media bridge listening on ${PORT}`));
