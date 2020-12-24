
"use strict";

/* adapted from node.js docs */
const express = require('express');
const database = require('./database.js');
const evFilt = require('./eventFilter.js');
const ejs = require('ejs');

const port = 8080;
const app = express();

let buffer = '';
let prevTime = new Map();
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

const HTTP_REQ_LATENCY_SECS = 1;
const SECS_PER_PING = 1;
const SWEEP_CHECK_FREQ = 1;

setInterval(()=>{
    const curr = Date.now();
    for (const [email, time] of prevTime) {
        if(curr-time >= 1000*(SECS_PER_PING+HTTP_REQ_LATENCY_SECS)){
            let predAc = prevAccepted.get(email);
            db.insert(email, predAc.url, predAc.wasted, predAc.time, curr);
            console.log(JSON.stringify({"type":3, "url":null, "time":curr}));
            prevTime.delete(email);
        }
    }
}, 1000*SWEEP_CHECK_FREQ);

app.route('/')
    .post((req, res) => {
        req.on('data', (data) => {
            buffer += data.toString();
        });

        req.on('end', () => {
            let packet = JSON.parse(buffer);
            let email = packet.id;
            let ev = packet.data;

            let pred = prevReceived.get(email);
            let predAc = prevAccepted.get(email);

            console.log(JSON.stringify(ev));

            // overwrites with different type, should be fine in JS.
            let restCond = (ev.url = evFilt.isProperEvent(ev, pred)) != null && pred !== undefined;
            
            if(restCond && predAc !== undefined){
                db.insert(email, predAc.url, predAc.wasted, predAc.time, ev.time);
                prevAccepted.set(email, ev);
            } else if(restCond){
                prevAccepted.set(email, ev);
            }
            prevReceived.set(email, ev);

            buffer = '';
        });
        
        res.sendStatus(200);
    })

    .head((req, res) => {
        let email = req.query.id;
        prevTime.set(email, Date.now());
        res.sendStatus(200);
    });

app.route('/summary')
    .get((req, res) => {
        let email = req.query.id;
        currResult = res;
        db.getUserSummary(email);
    });

app.route('/noteWasted')
    .head((req, res) => {
        let email = req.query.id;
        let pred = prevAccepted.get(email);

        if(pred !== undefined){
            pred.wasted = true;
        }

        res.sendStatus(200);
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