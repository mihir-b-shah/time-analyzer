
"use strict";

const sqlite = require('sqlite3').verbose();
const evem = require('events');

class Database extends evem.EventEmitter {

    // make sure this is called from the server directory.
    constructor(){
        super();
        this.db = new sqlite.Database('./users.db', (err) => {
            if (err) {
                console.error(err.message);
            }
            console.log('Connected to the user database.');
        });

        this.opQ = new Map();
        this.valueWatcher = new evem.EventEmitter()
    }

    incrementOpQ(email){
        if(this.opQ.has(email)){
            this.opQ.set(email, 1+this.opQ.get(email));
        } else {
            this.opQ.set(email, 1);
        }
    }

    decrementOpQ(email){
        let v = null;
        if((v = this.opQ.get(email)) == 1){
            this.opQ.delete(email);
        } else {
            this.opQ.set(email, v-1);
        }
    }

    queueEmpty(email){
        return this.opQ.get(email) == 0;
    }

    insert(email, url, wasted, start, end){
        const _email = email.substr(0, Math.min(email.length, 256));
        const _host = url.hostname.substr(0, Math.min(url.hostname.length, 128));
        const _url = url.href.substr(0, Math.min(url.href.length, 512));

        const InsertEvent =
            'insert into Events (email, url, host, wasted, start, end) '+
            `values ('${_email}', '${_url}', '${_host}', '${wasted}', '${start}', '${end}');`

        this.incrementOpQ(email);
        this.db.run(InsertEvent, (err)=>{
            if(err !== null){
                this.emit('error', err.message + 'prob in insert occurred.');
            } else {
                this.emit('insert');
            }
            this.decrementOpQ(email);
            this.valueWatcher.emit('finished');
        });
    }

    unsyncUserSummary(email){
        const GetUserData = 
            'select host as hostname, sum(end-start) as totalTime from Events '+
            `where email = '${email}' `+
            'group by host '+
            'order by totalTime desc;';

        this.db.all(GetUserData, (err, rows) => {
            if(err !== null){
                this.emit('error', err.message);
            } else {
                this.emit('summary', rows);
            }
        });
    }

    async getUserSummary(email){
        if(this.queueEmpty(email)){
            this.valueWatcher.on('finished', ()=>{
                this.unsyncUserSummary(email);
            });
        } else {
            this.unsyncUserSummary(email);
        }
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