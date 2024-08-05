let numberCurrentContact = "";
let socketsConnection = [];

const getConversations = async () => {
  const response = await fetch("/all/numbers");
  const data = await response.json();
  return data.contacts;
};

const filterContact = (event) => {
    const $contentContacts = document.getElementById("content-contacts");
    const $contacts = $contentContacts.getElementsByTagName("li");
    const value = event.target.value.toLowerCase();
    for (let contact of $contacts) {
        const name = contact.getElementsByClassName("name")[0].innerText.toLowerCase();
        if (name.indexOf(value) > -1) {
        contact.style.display = "";
        } else {
        contact.style.display = "none";
        }
    }
}

const initShowConversations = async () => {
  let contacts = localStorage.getItem("contacts");
  if (!contacts) {
    contacts = await getConversations();
    localStorage.setItem("contacts", JSON.stringify(contacts));
  }

  const $contentContacts = document.getElementById("content-contacts");
  if (typeof contacts === "string") contacts = JSON.parse(contacts);
  for (let contact of contacts) {

    let $li = document.createElement("li");
    $li.className = "clearfix";
    $li.addEventListener("click", () => selectContact(contact));
    const html = `
        <img
            src=${contact["image"]}
            alt="avatar"
        />
        <div class="about">
            <div class="name">${contact["name"]}</div>
            <small>${contact["number"]}</small>
        </div>
    `;
    $li.innerHTML = html;
    $contentContacts.appendChild($li);
  }
};

const get_feelings = async (number) => {
    const response = await fetch("/feelings/" + number);
    const data = await response.json();
    return data.average_starts;
}

const selectContact = async(contact) => {
    const $nameCurrentContact = document.getElementById("name-current-contact");
    const $avatarCurrentContact = document.getElementById("avatar-current-contact");
    const $contentMessagesAll = document.getElementById("content-all");
    $contentMessagesAll.style.scrollBehavior = "smooth";
    $contentMessagesAll.scrollTop = 0;

    $nameCurrentContact.innerText = contact["name"];
    $avatarCurrentContact.src = contact["image"];
    const $hiddenChat = document.getElementById("hidden-chat");
    $hiddenChat.style.display = "none";
    const $loadConversation = document.getElementById("load-conversation");
    $loadConversation.style.display = "flex";

    const response = await fetch("/conversation/" + contact["number"]);
    numberCurrentContact = contact["number"];
    const data = await response.json();
    const messages = data.messages;
    const $contentMessages = document.getElementById("content-messages");
    $contentMessages.innerHTML = "";
    let createdAtMessages = []

    for (let message of messages) {
        const $message = document.createElement("li");
        $message.className = 'clearfix';
        let html = ""
        if(message['from'] == contact['number'])
        {
            html = `
                <div class="message-data text-right" style="margin-right: 10px;">
                    <small class="message-data-time">${message['created_at']}</small>
                </div>
                <div class="message other-message float-right message-server">
                    ${message['message']}
                </div>
            `
        }
        else {
            html = `
                <div class="message-data" style="margin-right: 10px;">
                    <small class="message-data-time">${message['created_at']}</small>
                </div>
                <div class="message my-message message-server">${message['message']}</div>
            `
        }
        $message.innerHTML = html;
        $contentMessages.appendChild($message);
        createdAtMessages.push(message['created_at']);
    }
    $loadConversation.style.display = "none";
    const averageFeeling = await get_feelings(contact["number"]);
    let messageFeeling = "";
    if(averageFeeling <= 0.2) messageFeeling = "Esta super feliz 😄";
    if(averageFeeling > 0.2 && averageFeeling <= 0.4) messageFeeling = "Esta feliz 😊";
    if(averageFeeling > 0.4 && averageFeeling <= 0.5) messageFeeling = "Esta normal 😐";
    if(averageFeeling > 0.5 && averageFeeling <= 0.7) messageFeeling = "Esta enojado 😠"
    if(averageFeeling > 0.7 && averageFeeling <= 1) messageFeeling = "Esta super enojado 😡";
    const $feeling = document.getElementById("feeling");
    $feeling.innerText = messageFeeling;

    // sockets
    for (let socket of socketsConnection) socket.close();
    socketsConnection = [];
    const webSocket = new WebSocket("ws://localhost:8765");
    webSocket.addEventListener('open', (event) => webSocket.send(contact["number"]));
    webSocket.addEventListener('message', function (event) {

        let data = JSON.parse(event.data);
        for (let i = 0; i < data.length; i++)
        {
            const createAtMessageSocket = data[i]['created_at'];            
            const date = new Date(createAtMessageSocket);
            const formattedDate = date.toISOString().slice(0, 19);

            if(!createdAtMessages.includes(formattedDate))
            {
                const $message = document.createElement("li");
                $message.className = 'clearfix';
                let html = ""
                if(data[i].from == contact['number'])
                {
                    html = `
                        <div class="message-data text-right" style="margin-right: 10px;">
                            <small class="message-data-time">${formattedDate}</small>
                        </div>
                        <div class="message other-message float-right message-server">
                            ${data[i].message}
                        </div>
                    `
                }
                else {
                    html = `
                        <div class="message-data" style="margin-right: 10px;">
                            <small class="message-data-time">${formattedDate}</small>
                        </div>
                        <div class="message my-message message-server">${data[i].message}</div>
                    `
                }
                $message.innerHTML = html;
                $contentMessages.appendChild($message);
                createdAtMessages.push(formattedDate);
            }

        }
    });
    
    socketsConnection.push(webSocket);
}

const questionAboutChat = async(event) => {

    let contentMessages = "";
    if(event.type === "click") {
        contentMessages = document.getElementById("question").value;
    }
    else if(event.keyCode === 13) {
        contentMessages = document.getElementById("question").value;
    }

    if(contentMessages)
    {
        document.getElementById("question").disabled = true;
        const response = await fetch("/search/info/" + numberCurrentContact + "/" + contentMessages);
        const data = await response.json();
        const message = data.messages;
        const $predictResponse = document.getElementById("question-response");
        const $titleQuestion = document.getElementById("question-user");
        $predictResponse.innerText = message;
        $titleQuestion.innerText = contentMessages;
        var myModal = new bootstrap.Modal(document.getElementById('question-modal'), {
            keyboard: false
          });
        myModal.show();
        document.getElementById("question").value = "";
        document.getElementById("question").disabled = false;
    }
}

const predictAboutChat = async() => {
    document.getElementById("predict-response").innerText = "Pensando 🥱";
    var myModal = new bootstrap.Modal(document.getElementById('predict-modal'), {
        keyboard: false
      });
    myModal.show();
    document.getElementById("title-predict").innerText = "Predicción 🧙‍♂️";
    const response = await fetch("/preddict/message/" + numberCurrentContact + "/type/predict");
    const data = await response.json();
    const message = data.message;
    document.getElementById("predict-response").innerText = message;

}

const adviceAboutChat = async() => {
    document.getElementById("predict-response").innerText = "Pensando 🥱";
    var myModal = new bootstrap.Modal(document.getElementById('predict-modal'), {
        keyboard: false
      });
    myModal.show();
    document.getElementById("title-predict").innerText = "Consejo 🦆";
    const response = await fetch("/preddict/message/" + numberCurrentContact + "/type/advice");
    const data = await response.json();
    const message = data.message;
    document.getElementById("predict-response").innerText = message;
}

// invokes 🧙‍♂️🐲

document.getElementById("search").addEventListener("keyup", filterContact);
document.getElementById("question").addEventListener('keyup', questionAboutChat);
document.getElementById("question-buttom").addEventListener('click', questionAboutChat);
document.getElementById("predict-buttom").addEventListener('click', predictAboutChat);
document.getElementById("advice-buttom").addEventListener('click', adviceAboutChat);
initShowConversations();