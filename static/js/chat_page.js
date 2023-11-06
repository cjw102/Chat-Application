let timeoutID;
let timeout = 15000;


window.addEventListener('load', setup);

function setup()
{
    displayMessages();
    timeoutID = window.setTimeout(poller, timeout);
}


function displayMessages()
{
 
    fetch("/messages/")
    .then((response) => {
        return response.json();
    })
    .then((results) => {

        let chat_window = document.getElementById("chatlog");
        let messages = "";

        for(let i = 0; i < results.chats.length; i++)
        {
            author = results.chats[i]["author"];
            msg = results.chats[i]["content"];       
            messages += `${author}: ${msg}\n\n`;
        }

        chat_window.value = messages;
        
    })
    .catch(err => console.log("Error:", err));

    timeoutID = window.setTimeout(poller, timeout);
        
}

function poller()
{
    fetch("/messages/")
    .then((response) => {
        return response.json();
    })
    .then(() => displayMessages())
    .catch(err => console.log("Error:", err));
}