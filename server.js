
"use strict";

/* adapted from node.js docs */
const http = require('http');

const hostname = '127.0.0.1'; // localhost
const port = 8080;

// js excuse for an enum
const EventType = Object.freeze({
    ACTIVATE : 0,
    UPDATE   : 1,
    FOCUS    : 2,
    SENTINEL : 3
}); 

let buffer = null;
let prevReceived = null;
let prevAccepted = null;

/* unifies all invalid reasons to null */
function cleanURL(urlStr){
    if(urlStr === undefined){
        return null;
    }
    // simplest way to check if url is valid.
    let url = null;
    try {
        url = new URL(urlStr);
    } catch (error) {
        return null;
    }
    switch(url.protocol){
        case 'http:':
        case 'https:':
            return url.hostname;
        default:
            return null;
    }
}

function isProperEvent(ev){    
    url = cleanURL(ev.url);
    
    if(url === null){
        return false;
    }
    
    if(ev.type == EventType.UPDATE && prevRecived !== null &&
        prevReceived.type == EventType.ACTIVATE && prevReceived !== prevAccepted){
        return false;
    }

    return true;
}

// change this to real emails.
const server = http.createServer((req, res) => {
    req.on('data', (data) => {
        buffer += data.toString();
    });

    req.on('end', () => {
        events = JSON.parse(buffer);

        for(ev of events){
            if(isProperEvent(ev)){
                // ev.url, prevAccepted.time, ev.time
                prevAccepted = ev;
            }
            prevReceived = ev;
        }
        
        buffer = '';
    });
    
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end();
});

server.listen(port, hostname, () => {
    buffer = '';

    console.log(`Server running at http://${hostname}:${port}/`);
});