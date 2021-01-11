
"use strict";

/* --------------------- mutable state ------------------------- */

/* maps window id -> tab id */
let activeTabs = new Map();

/* maps tab id -> tab object */
let tabIds = new Map();

/* previous focused window, it is guaranteed that on()
   will get called to initialize this. */
let topWindowId = null;

/* cache the user's email */
let userEmail = null;

/* --------------------- types --------------------------------- */

const CallerType = Object.freeze({
    ACTIVATE : 0,
    UPDATE   : 1,
    FOCUS    : 2
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
        this.wasted = false;
        
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

async function stillHere(){
    const res = await fetch('http://localhost:8080?'+ new URLSearchParams(
        {'id':userEmail}), {method: "HEAD"});
}

setInterval(stillHere, 1000);

/* this is dangerous, possibly causes race condition */
window.onload = (event) => {
    chrome.windows.getAll((windows) => {
        for(let win of windows){
            if(win.focused){
                topWindowId = win.id;
            }
            chrome.tabs.getAllInWindow(win.id, (tabs) => {
                for(let tab of tabs){
                    if(tab.active){
                        activeTabs.set(win.id, tab.id);
                    }
                    tabIds.set(tab.id, tab);
                }

                // finally get the user email.
                chrome.identity.getProfileUserInfo((info)=>{
                    userEmail = info.email;
                    recordEvent(0);
                });
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

async function sendEvent(cleanup, ev){
    const res = await fetch("http://localhost:8080", { 
        method: "POST",
        
        body: JSON.stringify({'id':userEmail, 'data':ev}), 

        headers: { 
            "Content-type": "application/json; charset=UTF-8"
        } 
    });
    
    cleanup();
    
    if(!res.ok){
        throw new ExtensionError('Recent user event not sent.');
    }
}

function recordEvent(callerType){    
    sendEvent(()=>{}, new UserEvent(callerType));
}

function endSession(){
    // reset everything in case.
    activeTabs = new Map();
    tabIds = new Map();
    topWindowId = null;
}

/* ------------------------ DOM -------------------------------- */

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('summary').addEventListener('click', function() {
        chrome.tabs.create({'url':'http://localhost:8080/summary?' 
                + new URLSearchParams({'id':userEmail})}, (res)=>{});
    });

    document.getElementById('label').addEventListener('click', function() {
        chrome.tabs.create({'url':'http://localhost:5050/labeling?' 
                + new URLSearchParams({'id':userEmail})}, (res)=>{});
    });
});

/* ------------------- blocker --------------------------------- */

function modifyDOM() {
    return document.documentElement.innerText;
}

const BlockPageCode = 'BLOCK';

//We have permission to access the activeTab, so we can call chrome.tabs.executeScript:
chrome.history.onVisited.addListener((historyItem) => {
    if(historyItem.url !== undefined && historyItem.url.startsWith('http')){
        chrome.tabs.executeScript({
            code: '(' + modifyDOM.toString() + ')();'
        }, (text) => {
            fetch("http://localhost:5050/decide", { 
                method: "POST",
                
                body: JSON.stringify({'id':userEmail, 'data':text}), 

                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                } 
            }).then((res) => {
                res.text()
                    .then((txt) => {
                        if(txt === BlockPageCode){
                            chrome.tabs.update({'url': 'blocked.html'})
                        }
                    }).catch((err) => {});
            }).catch((err) => {});
        });
    }
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