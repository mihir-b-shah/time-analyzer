
/* unifies all invalid reasons to null */
function cleanURL(urlStr){
    if(urlStr === undefined){
        return null;
    }
    // simplest way to check if url is valid.
    let url = null;
    try {
        url = new URL(urlStr);
    } catch (error) {
        return null;
    }
    switch(url.protocol){
        case 'http:':
        case 'https:':
            return url;
        default:
            return null;
    }
}

/** returns null if event is improper */
exports.isProperEvent = function(ev, prev){    
    let url = cleanURL(ev.url);
    
    if(url === null){
        return null;
    }
    
    if(prev !== undefined && prev.url === ev.url){
        return null;
    }

    return url;
}