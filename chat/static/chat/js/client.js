function p(text, value) {
    console.log(text);
    console.log(value);
}

let chat = document.getElementById("chatBox");
let input = document.getElementById("inputBox");
input.addEventListener('keyup', submitText);

let chatHandler;
let source = {
    'email': document.getElementById('email').innerText,
    'full_name': document.getElementById('full_name').innerText,
};
let endpoint;
p('Current source', source)

const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">';
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">';
const closingTags = '</p></div></div></div>';
/*
Chat Handler
 */
chatHandler = new WebSocket(
    'wss://' + window.location.host + '/wss/chat/'
);
p('Chat handler: ', chatHandler)
chatHandler.addEventListener('open', startChat);
chatHandler.addEventListener('message', listenChat);

function startChat(e) {
    let data = {
        'action': 'init',
        'source': source,
    };
    p('Data sent: ', data)
    chatHandler.send(JSON.stringify(data));
}

function listenChat(e) {
    const data = JSON.parse(e.data);
    console.log('-------------------Receiver Data------------------- ')
    p('Current source: ', source);
    p('Current endpoint: ', endpoint);
    p('Data received: ', data);
    if (data['action'] === 'unavailable') {
        // checking if the request source is this websocket
        if (data['source']['email'] === source['email']) {
            if (!('endpoint' in data)) {
                input.disabled = true;
                addYourMessage('<i>No operatos available.</i>');
            }
        }
    } else if (data['action'] === 'init') {
        // checking if the request source is this websocket
        if (data['source']['email'] === source['email']) {
            if ('endpoint' in data) {
                endpoint = data['endpoint'];
                document.querySelector('#fullnameSpan').textContent = endpoint['full_name'];
                document.querySelector('#emailSpan').textContent = endpoint['email'];
                addYourMessage('Hello, how can I help you?');
            }
        }
    } else if (data['action'] === 'close') {
        if (source['email'] === data['endpoint_email']) {
            addYourMessage('<i>This chat has been closed.</i>');
            input.disabled = true;
            chatHandler.close();
        } else if (endpoint['email'] === data['endpoint_email']) {
            addYourMessage('<i>This chat has been closed.</i>');
            input.disabled = true;
            chatHandler.close();
        }
    } else if (data['action'] === 'message') {
        // checking if the message is FROM me
        // so it will only appear after the servers echos it back
        // to the corresponding consumers
        // this way we know for sure that the server received the message
        if (data['source']['email'] === source['email']) {
            addMyMessage(data['message']);
        }


        // checking if the message is for me
        if (data['endpoint']['email'] === source['email']) {
            // checking if the message is sent from the correct source
            if (data['source']['email'] === endpoint['email']) {
                addYourMessage(data['message']);
            }
        }
    }
}

// THE INPUT BOX
function submitText(e) {
    if (e.keyCode === 13) {
        let text = input.value;
        if (text !== '') {
            console.log('-------------------Sender data------------------- ')
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

function addYourMessage(msg) {
    chat.innerHTML += (yourMsg + msg + closingTags);
}

function addMyMessage(msg) {
    chat.innerHTML += (myMsg + msg + closingTags);
}