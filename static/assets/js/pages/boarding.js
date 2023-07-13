
const chatbox = document.querySelector("#chatbox");

// Function to scroll to the bottom of the chatbox
function scrollToBottom() {
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Scroll to bottom when the page is loaded
scrollToBottom();


const roomName = JSON.parse(document.getElementById('room_slug').textContent);
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/boarding/" + roomName + "/");
// const chatSocket = new WebSocket("ws://127.0.0.1:8000/ws/"+ roomName +"/");
// alert(chatSocket);
chatSocket.onopen = function (e) {
    console.log("The connection was setup successfully !");
};
chatSocket.onclose = function (e) {
    console.log("Something unexpected happened !");
};

document.querySelector("#my_input").focus();
document.querySelector("#my_input").onkeyup = function (e) {
    if (e.keyCode == 13) {
        e.preventDefault();
        document.querySelector("#submit_button").click();
    }
};
document.querySelector("#submit_button").onclick = function (e) {
    var messageInput = document.querySelector(
        "#my_input"
    ).value;
    const namaLengkap = JSON.parse(document.getElementById('nama_lengkap').textContent);
    const idUser = JSON.parse(document.getElementById('token').textContent);
    const FotoUser = JSON.parse(document.getElementById('fotoProfile').textContent);



    if (messageInput.length == 0) {
        alert("Add some Input First Or Press Send Button!")
    }
    else {
        chatSocket.send(JSON.stringify(
            {
                message: messageInput, id_user: idUser,
                id_kelas: 2,
                nama: namaLengkap,
                image: FotoUser
            }));


    }

};

const idUsers = JSON.parse(document.getElementById('token').textContent);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    var div = document.createElement("div");
    div.classList.add("chat-body");

    var chatMessage = document.createElement("div");
    chatMessage.classList.add("chat-message", "mt-4");
    
    dFlexItem = "justify-content-start"; // justify-content-end
    xFlexW100Item = "flex-row"; // "flex-row-reverse"


    var avatar = document.createElement("div");
    if (data.id_user == idUsers){
        avatar.classList.add("avatar", "avatar-md", "ms-3","me-4");
        dFlexItem = "justify-content-end"; // justify-content-end
        xFlexW100Item = "flex-row-reverse"; // "flex-row-reverse"
    }else{
        avatar.classList.add("avatar", "avatar-md", "me-3");

    }
    
    var dFlex = document.createElement("div");
    dFlex.classList.add("d-flex", "align-items-start",dFlexItem);

    var img = document.createElement("img");
    img.src = data.image;
    img.alt = "avatar";

    var dFlexW100 = document.createElement("div");
    dFlexW100.classList.add("d-flex", xFlexW100Item);

    var content = document.createElement("div");
    content.innerHTML = "<p class='mb-1' style='font-size: 14px;'><b>" + data.nama + "</b></p>" +
        "<small style='font-size: 14px;'>" + data.message + "</small>";

    dFlexW100.appendChild(content);
    avatar.appendChild(img);
    if (data.id_user == idUsers){
        dFlex.appendChild(dFlexW100);
        dFlex.appendChild(avatar);
    }else{
        dFlex.appendChild(avatar);
        dFlex.appendChild(dFlexW100);
    }
    chatMessage.appendChild(dFlex);
    div.appendChild(chatMessage);

    document.querySelector("#my_input").value = "";
    document.querySelector("#chatbox").appendChild(div);

    scrollToBottom();
};