document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const fileUpload = document.getElementById('file-upload');
    const chatHistory = document.getElementById('chat-history');

    // Function to update chat history
    function updateChatHistory(message, isUser) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.className = isUser ? 'user-message' : 'bot-message'; // Add class for styling
        chatHistory.appendChild(messageElement);
    }

    // Function to send messages to Langchain
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
            updateChatHistory(data.response, false);
        })
        .catch(error => console.error('Error:', error));
    }

    // Send message on button click
    sendButton.addEventListener('click', () => {
        const userMessage = chatInput.value.trim();
        if (userMessage) {
            updateChatHistory(userMessage, true);
            sendMessageToLangchain(userMessage);
            chatInput.value = '';
        }
    });

    // Send message on pressing 'Enter'
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    // Function to handle file uploads
    fileUpload.addEventListener('change', () => {
        const file = fileUpload.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/process-file', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                updateChatHistory(data.insights, false);
            })
            .catch(error => console.error('Error uploading file:', error));
        } else {
            updateChatHistory('No file selected for upload.', false);
        }
    });
});
