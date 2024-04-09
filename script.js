document.getElementById('send-btn').addEventListener('click', function() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (message) {
        sendMessage(message);
        messageInput.value = ''; // Clear input after sending
    }
});

function sendMessage(message) {
    // Here you would call your Azure Function
    console.log('Sending message:', message);
    // Dummy function to display message
    displayMessage(message, 'You');
}

function displayMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.textContent = `${sender}: ${message}`;
    msgDiv.className = 'message'; // Apply the message class for styling
    document.body.insertBefore(msgDiv, chatBox.nextSibling); // Place message in the body, after the chat-box
}


