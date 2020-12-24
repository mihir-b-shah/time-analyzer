
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
let prevAccepted = new Map();
let db = new database.Database();
let currResult = null;

function initDB(){
    db.on('error', (msg)=>{
        console.log('error in sql query: ' + msg);
    });
    
    db.on('insert', ()=>{
    });

    db.on('summary', (rows)=>{

        function fmtTime(millis){
            const secs = Math.floor(millis/1000);
            if(secs >= 60){
                const minutes = Math.floor(secs/60);
                if(minutes >= 60){
                    const hours = Math.floor(minutes/60);
                    return `${hours} hour(s), ${minutes%60} minute(s), ${secs%60} second(s)`
                } else {
                    return `${minutes} minute(s), ${secs%60} second(s)`
                }
            } else {
                return `${secs} second(s)`;
            }
        }

        for(let v of rows){
            v.totalTime = fmtTime(v.totalTime);
        }
        currResult.render('summary', {webpages:rows});
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
        let predAc = null;

        for(let ev of events){

            console.log(JSON.stringify(ev));

            pred = prevReceived.get(email);
            predAc = prevAccepted.get(email);

            let restCond = (ev.url = evFilt.isProperEvent(ev, pred)) != null && pred !== undefined;

            // overwrites with different type, should be fine in JS.
            if(restCond && predAc !== undefined){
                // console.log(`email: ${email}, url: ${predAc.url}, start time: ${predAc.time}, end time: ${ev.time}`);
                db.insert(email, predAc.url, predAc.time, ev.time);
                prevAccepted.set(email, ev);
            } else if(restCond){
                prevAccepted.set(email, ev);
            }
            prevReceived.set(email, ev);
        }
        console.log('boom!');
        
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