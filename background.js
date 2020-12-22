
"use strict";

/* --------------------- mutable state ------------------------- */

/* maps window id -> tab id */
let activeTabs = new Map();

/* maps tab id -> tab object */
let tabIds = new Map();

/* previous focused window, it is guaranteed that on()
   will get called to initialize this. */
let topWindowId = null;

/* avoids making post request every time */
let eventBuffer = [];

const EVENT_BUF_MAX_SIZE = 10;

/* --------------------- types --------------------------------- */

const CallerType = Object.freeze({
    ACTIVATE : 0,
    UPDATE   : 1,
    FOCUS    : 2,
    SENTINEL : 3
});

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
class ExtensionError extends Error {
    constructor(...params){
        super(...params);

        if(Error.captureStackTrace){
            Error.captureStackTrace(this, ExtensionError);
        }

        this.name = 'ExtensionError';
    }
};

class UserEvent {
    constructor(type){
        this.type = type;
        
        let tabIdRes = null;
        let tabRes = null;
        
        if (topWindowId !== null &&
           (tabIdRes = activeTabs.get(topWindowId)) !== undefined && 
           (tabRes = tabIds.get(tabIdRes)) !== undefined){
            this.url = tabRes.url;
        }

        this.time = Date.now();
    }
};

/* --------------------- initializers -------------------------- */

/* this is dangerous, possibly causes race condition */
window.onload = (event) => {
    chrome.windows.getAll((windows) => {
        for(win of windows){
            if(win.focused){
                topWindowId = win.id;
            }
            chrome.tabs.getAllInWindow(win.id, (tabs) => {
                for(tab of tabs){
                    if(tab.active){
                        activeTabs.set(win.id, tab.id);
                    }
                    tabIds.set(tab.id, tab);
                }
            });
        }
    });
}

/* --------------------- helpers ------------------------------- */

function log(msg){
    chrome.extension.getBackgroundPage().console.log(msg);
}

function removeTabFromWindow(winPtr, tabPtr){
    if(activeTabs.get(winPtr) === tabPtr){
        activeTabs.delete(winPtr);
    }
}

function ifCurrentWindow(winID, func, param){
    if(topWindowId === winID){
        func(param);
    }
}

async function sendEvent(cleanup){
    const res = await fetch("http://localhost:8080", { 
        method: "POST",
        
        body: JSON.stringify(eventBuffer), 

        headers: { 
            "Content-type": "application/json; charset=UTF-8"
        } 
    });
    
    cleanup();
    
    if(!res.ok){
        throw new ExtensionError('Recent user event not sent.');
    }
}

function sendAndClean(){
    sendEvent(()=>{
        eventBuffer = [];
    });
}

function recordEvent(callerType){    
    eventBuffer.push(new UserEvent(callerType));
    if(eventBuffer.length === EVENT_BUF_MAX_SIZE){
        sendAndClean();
    }
}

function endSession(){
    eventBuffer.push(new UserEvent(CallerType.SENTINEL));
    sendAndClean();
    
    // reset everything in case.
    activeTabs = new Map();
    tabIds = new Map();
    topWindowId = null;
}

/* ------------------- DOM callbacks --------------------------- */

document.addEventListener('DOMContentLoaded', function() {
    let link = document.getElementById('checkPage');
    /*
    link.addEventListener('click', function() {
        
    }); */
});

/* ------------------- tracking callbacks----------------------- */

chrome.tabs.onActivated.addListener(
    function actvAction(info){       
        activeTabs.set(info.windowId, info.tabId);
        ifCurrentWindow(info.windowId, recordEvent, CallerType.ACTIVATE);
    }
);

/* updates urls in tabIds when tab internally changes */
chrome.tabs.onUpdated.addListener(
    function updAction(id, info, tab){
        // only set if the url has changed.
        if(info.url !== undefined){
            tabIds.set(id, tab);
            ifCurrentWindow(tab.windowId, recordEvent, CallerType.UPDATE);
        }
    }
);

/*** NOTE THAT TAB CREATED FIRED WHEN USER CREATES ONE NOT WHEN ONE IS CREATED IN GENERAL ***/


/* if it is proper tab, add it to tabIds. We do not update activeTabs
   because onActivated() will do that for us- unless it is first tab.*/
chrome.tabs.onCreated.addListener(
    function crAction(tab){
        if(tab.id !== undefined){
            if(!activeTabs.has(tab.windowId)){
                activeTabs.set(tab.windowId, tab.id);
            }
            tabIds.set(tab.id, tab);
        }
    }
);

/* if it is the front of a window, remove it, and delete from tabIds. */
chrome.tabs.onRemoved.addListener(
    function remAction(id, info){
        removeTabFromWindow(info.windowId, id);
        tabIds.delete(id);
    }
);

/* if detached tab was active tab in that window, remove it */
chrome.tabs.onDetached.addListener(
    function detAction(id, info){
        removeTabFromWindow(info.oldWindowId, id);
    }
);

/* update topWindow if null */
chrome.windows.onCreated.addListener(
    function winCrAction(win){
        if(topWindowId === null || topWindowId === undefined){
            topWindowId = win.id;
        }
    }
);

/* going back to another page */
chrome.windows.onFocusChanged.addListener(
    function focAction(newID){
        if(newID != chrome.windows.WINDOW_ID_NONE){
            topWindowId = newID;
            recordEvent(CallerType.FOCUS);
        }
    }
);

/* if current page is closed. */
chrome.windows.onRemoved.addListener(
    function winRemAction(id){
        activeTabs.delete(id);
        if(topWindowId === id){
            topWindowId = null;
        }
        if(activeTabs.size == 0){
            endSession();
        }
    }
);