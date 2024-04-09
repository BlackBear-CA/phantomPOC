document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-btn');
    const uploadButton = document.getElementById('upload-btn');
    const messageInput = document.getElementById('message-input');
    const fileInput = document.getElementById('file-input');

    // Send text message to Langchain
    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            sendMessageToLangchain(message);
            messageInput.value = ''; // Clear input after sending
        }
    });

    // Upload file and get insights from Langchain
    uploadButton.addEventListener('click', function() {
        const file = fileInput.files[0];
        if (file) {
            uploadFile(file);
        }
    });

    // Send a message to Langchain and display response
    function sendMessageToLangchain(message) {
        fetch('/api/langchain-function', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: message })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(message, 'You');
            displayMessage(data.message, 'Langchain'); // Assuming 'data.message' contains the response
        })
        .catch(error => console.error('Error:', error));
    }

    // Upload file to the server for processing
    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/api/process-file', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Assuming 'data.insights' contains insights from the file
            updateChatHistory(data.insights, false); // Update chat with insights
        })
        .catch(error => console.error('Error uploading file:', error));
    }

    // Display message in chat history
    function displayMessage(message, sender) {
        const chatHistory = document.getElementById('chat-history');
        const msgDiv = document.createElement('div');
        msgDiv.textContent = `${sender}: ${message}`;
        msgDiv.className = 'message'; // Apply the message class for styling
        chatHistory.appendChild(msgDiv); // Add the new message div to the chat history
    }

    // Update chat history with insights or responses
    function updateChatHistory(message, isUserMessage) {
        const chatHistory = document.getElementById('chat-history');
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.className = isUserMessage ? 'user-message' : 'langchain-message';
        chatHistory.appendChild(messageDiv);
    }
});


