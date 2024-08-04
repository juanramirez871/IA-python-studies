let numberCurrentContact = "";


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
                <div class="message other-message float-right">
                    ${message['message']}
                </div>
            `
        }
        else {
            html = `
                <div class="message-data" style="margin-right: 10px;">
                    <small class="message-data-time">${message['created_at']}</small>
                </div>
                <div class="message my-message">${message['message']}</div>
            `
        }
        $message.innerHTML = html;
        $contentMessages.appendChild($message);
    }
    $loadConversation.style.display = "none";
    const averageFeeling = await get_feelings(contact["number"]);
    let messageFeeling = "";
    const averageFeelingRound = Math.ceil(averageFeeling);
    if(averageFeelingRound == 1) messageFeeling = "Esta super enojado 😡";
    if(averageFeelingRound == 2) messageFeeling = "Esta enojado 😠";
    if(averageFeelingRound == 3) messageFeeling = "Esta neutral 🧐";
    if(averageFeelingRound == 4) messageFeeling = "Esta feliz 😊";
    if(averageFeelingRound == 5) messageFeeling = "Esta super feliz 🥰";
    const $feeling = document.getElementById("feeling");
    $feeling.innerText = messageFeeling + " (" + averageFeelingRound + "/5)";
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
    const response = await fetch("/preddict/message/" + numberCurrentContact + "/type/predict");
    const data = await response.json();
    const message = data.message;
    document.getElementById("title-predict").innerText = "Predicción 🧙‍♂️";
    document.getElementById("predict-response").innerText = message;

}

const adviceAboutChat = async() => {
    document.getElementById("predict-response").innerText = "Pensando 🥱";
    var myModal = new bootstrap.Modal(document.getElementById('predict-modal'), {
        keyboard: false
      });
    myModal.show();
    const response = await fetch("/preddict/message/" + numberCurrentContact + "/type/advice");
    const data = await response.json();
    const message = data.message;
    document.getElementById("predict-response").innerText = message;
    document.getElementById("title-predict").innerText = "Consejo 🦆";
}

// invokes 🧙‍♂️🐲

document.getElementById("search").addEventListener("keyup", filterContact);
document.getElementById("question").addEventListener('keyup', questionAboutChat);
document.getElementById("question-buttom").addEventListener('click', questionAboutChat);
document.getElementById("predict-buttom").addEventListener('click', predictAboutChat);
document.getElementById("advice-buttom").addEventListener('click', adviceAboutChat);
initShowConversations();