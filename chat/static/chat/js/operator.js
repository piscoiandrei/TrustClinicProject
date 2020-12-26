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
listener.addEventListener('message', receivedData);
listener.addEventListener('close', listenerClose);
listener.addEventListener('error', listenerError);

function  listenerOpen(e){
    console.log('the listener just opened');
}

function listenerClose(e) {
    console.log('the listener ws just closed');
}

function listenerError(e) {
    console.log('an error occurred in the listener ws');
}

function receivedData(e) {
    const data = JSON.parse(e.data);
    console.log('the listener received data')
    if (data['available'] === 'true') {
        console.log(data);
    }
}

/*

 */
let chat = document.getElementById("chatBox");
let input = document.getElementById("inputBox");
input.addEventListener('keyup', submitText);

const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">';
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">';
const closingTags = '</p></div></div></div>';


let counter = 0;

function submitText(e) {
    if (e.keyCode == 13) {
        let text = input.value;
        if (text != '') {
            if (text.includes('1')) {
                chat.innerHTML += (myMsg + text + closingTags);
            } else {
                chat.innerHTML += (yourMsg + text + closingTags);
            }
            input.value = '';

            // here we are going to use the user id from the server
            counter = counter + 1;
            addMessageBox(counter);

            chat.scrollTop = chat.scrollHeight;
        }

    }
}

function addMessageBox(userId) {
    let leftCol = document.getElementById('left-col');

    let div = document.createElement('div');
    div.className = "shadow-sm mt-2 msg-box";
    div.id = userId;

    let span = document.createElement('span');
    span.className = "txt-sm";
    span.innerText = "User Full Name" + userId; // insert data from ws here

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
