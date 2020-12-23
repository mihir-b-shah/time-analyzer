
"use strict";

/* adapted from node.js docs */
const express = require('express');
const database = require('./database.js');
const evFilt = require('./eventFilter.js');
const ejs = require('ejs');

const port = 8080;
const app = express();

// js excuse for an enum
const EventType = Object.freeze({
    ACTIVATE : 0,
    UPDATE   : 1,
    FOCUS    : 2,
    SENTINEL : 3
}); 

let buffer = '';

let prevReceived = new Map();
let db = new database.Database();
let currResult = null;

function initDB(){
    db.on('error', (msg)=>{
        console.log('error in sql query: ' + msg);
    });
    
    db.on('insert', ()=>{
    });

    db.on('summary', (rows)=>{
        // render page.
        currResult.render('summary', {webpages:rows});
        currResult.sendStatus(200);
    });
}

app.post('/', (req, res) => {
    req.on('data', (data) => {
        buffer += data.toString();
    });

    req.on('end', () => {
        let packet = JSON.parse(buffer);
        let email = packet.id;
        let events = packet.data;
        let pred = null;

        for(let ev of events){
            pred = prevReceived.get(email);

            // overwrites with different type, should be fine in JS.
            if((ev.url = evFilt.isProperEvent(ev, pred)) != null && pred !== undefined){
                console.log(`email: ${email}, url: ${pred.url}, start time: ${pred.time}, end time: ${ev.time}`);
                db.insert(email, pred.url, pred.time, ev.time);
            }
            prevReceived.set(email, ev);
        }
        
        buffer = '';
    });
    
    res.sendStatus(200);
});

app.get('/summary', (req, res) => {
    let email = req.query.id;
    currResult = res;
    db.getUserSummary(email);
});

initDB();

app.set('views', __dirname);
app.set('view engine', 'ejs');

app.listen(port, function(error){ 
    if(error){
        throw error;
    } 
    console.log("Server created Successfully!"); 
}); 