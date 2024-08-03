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

const selectContact = (contact) => {
    const $nameCurrentContact = document.getElementById("name-current-contact");
    const $avatarCurrentContact = document.getElementById("avatar-current-contact");
    $nameCurrentContact.innerText = contact["name"];
    $avatarCurrentContact.src = contact["image"];
    const $hiddenChat = document.getElementById("hidden-chat");
    $hiddenChat.style.display = "none";
    const $loadConversation = document.getElementById("load-conversation");
    $loadConversation.style.display = "flex";
}

// invokes 🧙‍♂️🐲

document.getElementById("search").addEventListener("keyup", filterContact);
initShowConversations();
