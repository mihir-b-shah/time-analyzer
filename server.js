
/* adapted from node.js docs */
const http = require('http');

const hostname = '127.0.0.1'; // localhost
const port = 8080;

const server = http.createServer((req, res) => {
    console.log(JSON.parse(req.body));
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});