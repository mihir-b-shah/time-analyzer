
const express = require('express');
const ejs = require('ejs');

const app = express();

app.set('views', __dirname);
app.set('view engine', 'ejs');
  
app.get('/summary', function(req, res){ 
    people = [{'dimension':4,'quantity':5, 'factory':6}, {'dimension':1,'quantity':2, 'factory':3}, {'dimension':7,'quantity':8, 'factory':9}];
    res.render('summary', {quotation:people});
});
  
app.listen(8080, function(error){ 
    if(error){
        throw error;
    } 
    console.log("Server created Successfully!"); 
}); 