
console.log(email);
console.log(document);

async function sendToServer(){
    return await fetch("http://localhost:5050/decide", { 
        method: "POST",
        
        body: JSON.stringify({'id':email, 'doc':document}), 
    
        headers: { 
            "Content-type": "application/json; charset=UTF-8"
        } 
    });
}

sendToServer();