function p(text, value) {
    console.log(text);
    console.log(value);
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

let chat = document.getElementById("chatBox");
let input = document.getElementById("inputBox");
input.addEventListener('keyup', submitText);
input.disabled = true;

let chatHandler;
let source = {
    'email': document.getElementById('email').innerText,
    'full_name': document.getElementById('full_name').innerText,
};
let endpoint; // the current endpoint
p('Current source: ', source);

let chatCache = {};
let activeChats = {};
const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">';
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">';
const closingTags = '</p></div></div></div>';

/*
 ACTIVATOR Websocket
 */
let activator = new WebSocket(
    'wss://' + window.location.host + '/ws/chat/activator/'
);
activator.addEventListener('error', activatorErrorHandler);
activator.addEventListener('close', activatorClose);
activator.addEventListener('open', activatorOpen);

function activatorOpen(e) {
    console.log('The activator wss just opened');
}

function activatorClose(e) {
    console.log('The activator wss just closed');
}

function activatorErrorHandler(e) {
    // leave balnk for now
    // ideas:
    //https://stackoverflow.com/questions/3780511/reconnection-of-client-when-server-reboots-in-websocket
    console.log('an error occured in the activator wss');
}

/*
Chat Handler
 */

chatHandler = new WebSocket(
    'wss://' + window.location.host + '/ws/chat/'
);
p('Chat handler: ', chatHandler);
chatHandler.addEventListener('message', listenChat);

function listenChat(e) {
    const data = JSON.parse(e.data);
    console.log('-------------------Receiver Data------------------- ')
    p('Current source: ', source);
    p('Current endpoint: ', endpoint);
    p('Data received: ', data);

    // only the client can send init actions
    if (data['action'] === 'init') {
        // here we receive data, so the current source is the endpoint of the
        // other chat handler
        if (data['endpoint']['email'] === source['email']) {
            // if we don't have any active chats, we will set
            // the current active chat as the current one
            if (isEmpty(activeChats)) {
                endpoint = data['source']; //the client is our endpoint
                // now we initialize the chat for that user
                input.disabled = false;
                chatCache[endpoint['email']] = {
                    'source': [],
                    'endpoint': [],
                    'message': [],
                };
                activeChats[endpoint['email']] = {
                    'source': source,
                    'endpoint': endpoint,
                }
                document.querySelector('#fullnameSpan').textContent = endpoint['full_name'];
                document.querySelector('#emailSpan').textContent = endpoint['email'];
            } else {
                chatCache[data['source']['email']] = {
                    'source': [],
                    'endpoint': [],
                    'message': [],
                };
                activeChats[data['source']['email']] = {
                    'source': source,
                    'endpoint': data['source'],
                }
            }
            console.log(activeChats);

            // adding a message box with the given name and
            // the box id is the source's email (beacuse it's unique)
            addMessageBox(data['source']['full_name'], data['source']['email'])

        }
    } else if (data['action'] === 'close') {
        // we receive a close request from the client
        if (data['endpoint_email'] in activeChats) {

            delete activeChats[data['endpoint_email']];
            delete chatCache[data['endpoint_email']];
            removeMessageBox(data['endpoint_email']);
            // if this is the current endpoint we have to choose another
            if (endpoint['email'] === data['endpoint_email']) {
                endpoint = {};
                document.querySelector('#fullnameSpan').textContent = '-';
                document.querySelector('#emailSpan').textContent = '-';
                input.disabled = true;
                chat.innerHTML = '';
                input.innerHTML = '';
                alert('The client closed the connection, select another chat.')
            }
        }
    } else if (data['action'] === 'message') {
        // if we sent the message
        if (data['source']['email'] === source['email']) {
            // checking if the message is for this chat
            if (data['endpoint']['email'] === endpoint['email']) {
                chatCache[endpoint['email']]['source'].push(source);
                chatCache[endpoint['email']]['endpoint'].push(endpoint);
                chatCache[endpoint['email']]['message'].push(data['message']);
                addMyMessage(data['message']);
            }
        }

        // checking if the message if for me
        if (data['endpoint']['email'] === source['email']) {
            // if this from the current endpoint we cache and display
            if (data['source']['email'] === endpoint['email']) {
                // the source of the message is our endpoint
                chatCache[endpoint['email']]['source'].push(endpoint);
                // the endpoint of the message is us
                chatCache[endpoint['email']]['endpoint'].push(source);
                // caching the message
                chatCache[endpoint['email']]['message'].push(data['message']);

                addYourMessage(data['message']);
            } else {
                // just caaching the messages that are not from the current endpoint
                // the source of the message is our endpoint
                let key = data['source']['email'];
                chatCache[key]['source'].push(data['source']);
                // the endpoint of the message is us
                chatCache[key]['endpoint'].push(source);
                // caching the message
                chatCache[key]['message'].push(data['message']);
            }
        }


    }
    p('After processing the endpoint is: ', endpoint)
}

// INPUT BOX
function submitText(e) {
    if (e.keyCode === 13) {
        let text = input.value;
        if (text !== '') {
            console.log('-------------------Sender data------------------- ');
            let to_send = {
                'action': 'message',
                'source': source,
                'endpoint': endpoint,
                'message': text,
            }
            chatHandler.send(JSON.stringify(to_send));
            p('Data sent: ', to_send);
            input.value = '';
        }

    }
}

function addMessageBox(fullName, boxId) {
    let leftCol = document.getElementById('left-col');

    let div = document.createElement('div');
    div.className = "shadow-sm mt-2 msg-box";
    div.id = boxId;
    div.addEventListener('click', clickMessageBox)

    let span = document.createElement('span');
    span.className = "txt-sm";
    span.innerText = fullName;

    div.appendChild(span)

    let delBtn = document.createElement('a');
    delBtn.className = "float-right";

    let icon = document.createElement('i');
    icon.className = "fas fa-times";
    delBtn.appendChild(icon);

    delBtn.addEventListener('click', deleteMessageBox);

    div.appendChild(delBtn);

    leftCol.appendChild(div);

    leftCol.scrollTop = leftCol.scrollHeight;

}

function clickMessageBox(e) {
    let email = e.target.id;
    console.dir(e.target);
    p('The message box has been selected for: ', email);
    input.value = '';
    chat.innerHTML = '';
    // select endpoint
    endpoint = activeChats[email]['endpoint'];
    input.disabled = false;
    document.querySelector('#fullnameSpan').textContent = endpoint['full_name'];
    document.querySelector('#emailSpan').textContent = endpoint['email'];
    // load all messages
    let sources = chatCache[email]['source'];
    let endpoints = chatCache[email]['endpoint'];
    let messages = chatCache[email]['message'];

    for (let i = 0; i < sources.length; i++) {
        if (sources[i]['email'] === source['email']) {
            addMyMessage(messages[i]);
        } else if (endpoints[i]['email'] === source['email']) {
            addYourMessage(messages[i]);
        }
    }

}


function deleteMessageBox(e) {
    // preventing the del button to trigger a parent click event
    e.stopPropagation();
    // here we are closing the chat with the client
    let leftCol = document.getElementById('left-col');
    let msgBox = e.target.parentElement.parentElement;
    let email = msgBox.id;
    p('The close button has been clicked for: ', email)
    leftCol.removeChild(msgBox);
    // sending a message to the client so the other websocket knows
    // it has to terminate the connection
    console.log('-------------------Sender data------------------- ');
    let to_send = {
        'action': 'close',
        'endpoint_email': email,
    };

    chatHandler.send(JSON.stringify(to_send));
    p('Data sent: ', to_send);

    // if we close the current endpoint we will set is empty
    delete activeChats[email];
    delete chatCache[email];
    // if this is the current endpoint we have to choose another
    if (endpoint['email'] === email) {
        endpoint = {};
        document.querySelector('#fullnameSpan').textContent = '-';
        document.querySelector('#emailSpan').textContent = '-';
        input.disabled = true;
        chat.innerHTML = '';
        input.value = '';
        alert('You need to select a new chat or wait for a new connection.')
    }
}

function removeMessageBox(boxId) {
    // removing UI
    let leftCol = document.getElementById('left-col');
    leftCol.removeChild(document.getElementById(boxId))
}

function addYourMessage(msg) {
    chat.innerHTML += (yourMsg + msg + closingTags);
}

function addMyMessage(msg) {
    chat.innerHTML += (myMsg + msg + closingTags);
}