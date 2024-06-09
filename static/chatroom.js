let message = document.getElementById('message');
let chatLogs = document.querySelector('.logs');
let username = document.getElementById('username').value;

// Simulate a delay to show the typing indicator
let typingTimer;

function startTypingIndicator() {
    let indicator = document.querySelector('.typing-indicator');
    indicator.style.display = 'flex';
    typingTimer = setTimeout(function () {
        stopTypingIndicator();
    }, 2000); // Adjust the delay as needed
}

function stopTypingIndicator() {
    let indicator = document.querySelector('.typing-indicator');
    indicator.style.display = 'none';
    clearTimeout(typingTimer);
}

async function refreshChat() {
    let serverData = await fetch('/read_msg');
    let data = await serverData.json();
    let text = "";
    for (let i = 0; i < await data.length; i++)
        text = text + "[" + data[i].time + "] <b>" + data[i].username + ":</b> " + data[i].message + "<br />";
    chatLogs.innerHTML = text;
    chatLogs.scrollTop = chatLogs.scrollHeight;
}

setInterval(refreshChat, 1000);

function postMessage() {
    if (username != "") {
        if (message.value != "") {
            fetch('/send/' + username + '/' + message.value);
            message.value = "";
        } else {
            alert("Please enter a message!");
        }
    } else {
        alert("Anonymous messages are not allowed!");
    }
}

// Add event listener for the Enter key
message.addEventListener('keypress', function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        postMessage();
    }
});
