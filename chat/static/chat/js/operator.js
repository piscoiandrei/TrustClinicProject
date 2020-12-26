activeChats = {
    'chat_id': 'example',
    'operator': {
        'id': '',
        'fullname': '',
        'email': '',
    },
    'client': {
        'id': '',
        'fullname': '',
        'email': '',
        'phone': '',
    }
};
let chatHandler;
let currentSource = {};
let currentEndpoint = {};

let chat = document.getElementById("chatBox");
let input = document.getElementById("inputBox");
input.addEventListener('keyup', submitText);

const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">';
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">';
const closingTags = '</p></div></div></div>';

/*
 ACTIVATOR Websocket
 */
let activator = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/activator/'
);
activator.addEventListener('error', activatorErrorHandler);
activator.addEventListener('close', activatorClose);
activator.addEventListener('open', activatorOpen);

function activatorOpen(e) {
    console.log('The activator ws just opened');
}

function activatorClose(e) {
    console.log('The activator ws just closed');
}

function activatorErrorHandler(e) {
    // leave balnk for now
    // ideas:
    //https://stackoverflow.com/questions/3780511/reconnection-of-client-when-server-reboots-in-websocket
    console.log('an error occured in the activator WS');
}

/*

 */
/*
LISTENER WebSocket
 */
let listener = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/listener/'
);
listener.addEventListener('open', listenerOpen);
listener.addEventListener('message', listenerMessage);
listener.addEventListener('close', listenerClose);
listener.addEventListener('error', listenerError);

function listenerOpen(e) {
    console.log('the listener just opened');
}

function listenerClose(e) {
    console.log('the listener ws just closed');
}

function listenerError(e) {
    console.log('an error occurred in the listener ws');
}

function listenerMessage(e) {
    const data = JSON.parse(e.data);
    console.log('the listener received data')
    if (data['available'] === 'true') {
        /*
       Chat Handler
       */
        console.log(data);
        currentSource = data['operator'];
        currentEndpoint = data['client'];

        chatHandler = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + data['chat_id'] + '/'
        );
        chatHandler.addEventListener("open", chatHandlerOpen);
        chatHandler.addEventListener("message", chatHandlerMessage);
        chatHandler.addEventListener("close", chatHandlerClose);
        chatHandler.addEventListener("error", chatHandlerError);
    }
}


function chatHandlerOpen(e) {
    console.log('the chat handler just opened');
}

function chatHandlerMessage(e) {
    console.log('the chat handler just received a message');
    const data = JSON.parse(e.data);
    // received my own message from the server, now we display it
    if (data['source']['id'] === currentSource['id']) {
        addMyMessage(data['message']);
        input.value = '';
        chat.scrollTop = chat.scrollHeight;
    }
    if (data['endpoint']['id'] === currentSource['id']) {
        addYourMessage(data['message']);
        input.value = '';
        chat.scrollTop = chat.scrollHeight;
    }
}

function chatHandlerClose(e) {
    console.log('the chat handler just closed');
}

function chatHandlerError(e) {
    console.log('an error occurred in the chat handler');
}

/*

 */

// INPUT BOX
function submitText(e) {
    if (e.keyCode === 13) {
        let text = input.value;
        if (text !== '') {
            chatHandler.send(
                JSON.stringify(
                    {
                        'source': currentSource,
                        'endpoint': currentEndpoint,
                        'message': text,
                    }
                )
            )
            // we are going to display the message when we receive it back from
            // the server, so we know for sure that it has been sent
        }

    }
}

function addMessageBox(chatId) {
    let leftCol = document.getElementById('left-col');

    let div = document.createElement('div');
    div.className = "shadow-sm mt-2 msg-box";
    div.id = chatId;

    let span = document.createElement('span');
    span.className = "txt-sm";
    span.innerText = "User Full Name" + chatId; // insert data from ws here

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

function deleteMessageBox(e) {


    let leftCol = document.getElementById('left-col');
    let msgBox = e.target.parentElement.parentElement;
    leftCol.removeChild(msgBox);

    // then close the ws
    // myWebSocket.close();
}
function addYourMessage(msg) {
    chat.innerHTML += (yourMsg + msg + closingTags);
}

function addMyMessage(msg) {
    chat.innerHTML += (myMsg + msg + closingTags);
}