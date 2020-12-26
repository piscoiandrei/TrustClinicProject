let currentUserId = document.getElementById("id").innerText;
let chatHandler;
let chat = document.getElementById("chatBox");
let input = document.getElementById("inputBox");
input.addEventListener('keyup', submitText);

let currentSource = {}
let currentEndpoint = {}

const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">';
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">';
const closingTags = '</p></div></div></div>';
/*
LISTENER WebSocket
 */
let listener = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/listener/'
);
listener.addEventListener('open', listenerSendData);
listener.addEventListener('message', listenerMessage);
listener.addEventListener('close', listenerClose);
listener.addEventListener('error', listenerError);

function listenerClose(e) {
    console.log('the listener ws just closed');
}

function listenerError(e) {
    console.log('an error occurred in the listener ws');
}

function listenerSendData(e) {
    let data_to_send = {
        'id': currentUserId,
    };
    e.target.send(JSON.stringify(data_to_send));
}

function listenerMessage(e) {
    const data = JSON.parse(e.data);
    console.log('the listener received data');
    if (data['available'] === 'false') {
        if (data['endpoint'] === currentUserId) {
            input.disabled = true;
            addYourMessage('No operators available for now. Try again later.');
        }
    } else if (data['available'] === 'true') {
        //opening a chat handler with the given data if an operator is available
        /*
        Chat Handler
        */
        console.log(data);
        currentSource = data['client']
        currentEndpoint = data['operator']

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

    const data = JSON.parse(e.data)
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

// THE INPUT BOX
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

function addYourMessage(msg) {
    chat.innerHTML += (yourMsg + msg + closingTags);
}

function addMyMessage(msg) {
    chat.innerHTML += (myMsg + msg + closingTags);
}