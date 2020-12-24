let k = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/listener/'
)
k.addEventListener('open', sendData)
k = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/activator/'
)
k.addEventListener('open', sendData)

currentUser = JSON.stringify({
    'id': document.getElementById("id").innerText,
})

function sendData(e) {
    console.dir(e)
    e.target.send(currentUser)
}


let chat = document.getElementById("chatBox")
let input = document.getElementById("inputBox")
input.addEventListener('keyup', submitText)

const myMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-right shadow-sm txt-sm my-msg">'
const yourMsg = '<div class="row pt-2"><div class="col-12"><p class="pt-1 pb-1 pl-2 pr-2 text-white float-left shadow-sm txt-sm your-msg">'
const closingTags = '</p></div></div></div>'


let counter = 0

function submitText(e) {
    if (e.keyCode == 13) {
        let text = input.value
        if (text != '') {
            if (text.includes('1')) {
                chat.innerHTML += (myMsg + text + closingTags)
            } else {
                chat.innerHTML += (yourMsg + text + closingTags)
            }
            input.value = ''

            // here we are going to use the user id from the server
            counter = counter + 1
            addMessageBox(counter)

            chat.scrollTop = chat.scrollHeight
        }

    }
}

function addMessageBox(userId) {
    let leftCol = document.getElementById('left-col')

    let div = document.createElement('div')
    div.className = "shadow-sm mt-2 msg-box"
    div.id = userId

    let span = document.createElement('span')
    span.className = "txt-sm"
    span.innerText = "Operator FUllname" + userId // insert data from ws here

    div.appendChild(span)

    let delBtn = document.createElement('a')
    delBtn.className = "float-right"

    let icon = document.createElement('i')
    icon.className = "fas fa-times"
    delBtn.appendChild(icon)

    delBtn.addEventListener('click', deleteMessageBox)

    div.appendChild(delBtn)

    leftCol.appendChild(div)

    leftCol.scrollTop = leftCol.scrollHeight

}

function deleteMessageBox(e) {


    let leftCol = document.getElementById('left-col')
    let msgBox = e.target.parentElement.parentElement
    leftCol.removeChild(msgBox)

    // then close the ws
    // myWebSocket.close();
}
