
"use strict"

const fs = require('fs');
const fetch = require('node-fetch');
const shuffle = require('shuffle-array');

const NUM_LINES_PER_RECORD = 16;
const URL_RECORD_POS = 1;
const URL_POS_START = 20;
const DOC_BUFFER_SIZE = 1000;

let docs = [];
let processed = undefined;
let docCtr = 0;

async function getHTML(url){
    // console.log(url);
    fetch(url)
        .then((res)=>{
            if(!res.ok){
                throw res;
            } else {
                return res.text();
            }
        })
        .then((res)=>{
            docs.push(res);
        })
        .catch((err) => {
        })
        .finally(()=>{
            --processed;
            if(docs.length === DOC_BUFFER_SIZE || processed === 0){
                fs.writeFile(`../../../../data/docs/pages${++docCtr}.txt`, JSON.stringify(docs), (err)=>{
                    if(err !== null){
                        console.error('error in writing data file.');
                    }
                });
                docs = []; 
            }
        })
}

function run(){
    try {
        const data = fs.readFileSync('../../../../data/data.txt', 'utf-16le');
        const lines = data.split(/\r?\n/);

        let ctr = 0;
        let urls = new Set();

        lines.forEach((line) => {
            if(ctr % NUM_LINES_PER_RECORD == URL_RECORD_POS){
                let url = line.substring(URL_POS_START);
                // console.log(url);
                if(url.startsWith('http')){
                    urls.add(url);
                }
            }
            ++ctr;
        });


        urls = Array.from(urls);
        shuffle(urls, { 'copy': false });
        processed = urls.length;

        for(let url of urls){
            getHTML(url);
        }

    } catch (err) {
        console.error(err);
    }
}

run();
setInterval(()=>{
    console.log(processed);
}, 1000);
