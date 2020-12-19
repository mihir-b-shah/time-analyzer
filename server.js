
/* adapted from node.js docs */
const http = require('http');

const hostname = '127.0.0.1'; // localhost
const port = 8080;

let buffer = '';

const server = http.createServer((req, res) => {
    req.on('data', (data) => {
        buffer += data.toString();
    });

    req.on('end', () => {
        console.log(JSON.parse(buffer));
        buffer = '';
    });
    
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end();
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});