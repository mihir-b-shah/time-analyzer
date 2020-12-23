
"use strict";

const sqlite = require('sqlite3').verbose();
const evem = require('events');

class Database extends evem.EventEmitter {

    constructor(){
        super();
        this.db = new sqlite.Database('./users.db', (err) => {
                if (err) {
                    console.error(err.message);
                }
                console.log('Connected to the user database.');
            }
        );
    }

    padNumber(intg){
        return intg.toString().padStart(2,'0');
    }

    fmtDate(millis){
        const date = new Date(millis);
        return `${date.getFullYear()}${this.padNumber(1+date.getMonth())}${this.padNumber(date.getDate())} `+
                `${this.padNumber(date.getHours()%12)}:${this.padNumber(date.getMinutes())}:`+
                `${this.padNumber(date.getSeconds())} ${date.getHours()>=12?'PM':'AM'}`
    }

    insert(email, url, start, end){
        const _email = email.substr(0, Math.min(email.length, this.MaxEmailLength));
        const _host = url.hostname.substr(0, Math.min(url.hostname.length, this.MaxHostLength));
        const _url = url.href.substr(0, Math.min(url.href.length, this.MaxURLLength));

        const InsertEvent =
            'insert into Events (email, url, host, start, end) '+
            `values ('${_email}', '${_url}', '${_host}', '${this.fmtDate(start)}', '${this.fmtDate(end)}');`

        this.db.run(InsertEvent, (err)=>{
            if(err !== null){
                this.emit('error', 'insert');
            } else {
                this.emit('insert');
            }
        });
    }

    getUserSummary(email){
        const GetUserData = 
            'select host as hostname, sum(time) as totalTime from Events '+
            `where email = ${email} `+
            'group by host '+
            'order by totalTime desc;';

        this.db.all(GetUserData, (err, rows) => {
            if(err !== null){
                this.emit('error', 'select');
            } else {
                this.emit('summary', rows);
            }
        });
    }

    release(){
        this.db.close((err) => {
            if (err) {
                return console.error(err.message);
            }
            console.log('Closed the database connection.');
        });
    }
};

module.exports = {
    Database: Database
};