
"use strict";

const sqlite = require('sqlite3').verbose();

class Database {

    loadTable(){
        this.db = new sqlite.Database('./users.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE, 
            (err) => {
                if (err) {
                    console.error(err.message);
                }
                console.log('Connected to the user database.');
            }
        );
    }

    // mutations should run sequentially
    makeTable(){
        this.db.serialize();
        const BuildTable = 
            "create table if not exists Events ("+
                "email   varchar(255)   not null,"+
                "url     varchar(128)   not null,"+
                "start   datetime       not null,"+ 
                "end     datetime       not null "+
            ");";

        this.db.run(BuildTable, (err) => {
            if (err) {
                console.error(err.message);
            }
        });

        this.db.parallelize();
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

    // mutations should run sequentially
    insert(email, url, start, end){
        this.db.serialize();
        const InsertEvent =
            "insert into Events (email, url, start, end) "+
            `values ('${email}', '${url}', '${this.fmtDate(start)}', '${this.fmtDate(end)}');`

        this.db.run(InsertEvent, (err)=>{
            if(err){
                console.error(err.message);
            }
        });

        this.db.parallelize();
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