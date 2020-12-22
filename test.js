
const database = require('./database.js');

let dbse = new database.Database();
dbse.loadTable();
dbse.makeTable();
dbse.insert('mihirshah.11204@gmail.com', 'https://google.com', 1608614095646, 1608614096000);
dbse.insert('bipin.supriya@gmail.com', 'https://bing.com', 1608614096891, 1608614096911);
dbse.release();
