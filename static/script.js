const form = document.getElementById('chatForm');
const input = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const sendButton = document.getElementById('sendButton');

// Configure marked to use breaks for newlines
marked.setOptions({
    breaks: true
});

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addMessage(content, isUser = false) {
    const wrapper = document.createElement('div');
    wrapper.className = `message-wrapper ${isUser ? 'user' : 'assistant'}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    if (isUser) {
        bubble.textContent = content;
    } else {
        bubble.innerHTML = marked.parse(content);
    }
    
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    scrollToBottom();
}

function showTypingIndicator() {
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper assistant';
    wrapper.id = 'typingIndicator';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    
    bubble.appendChild(indicator);
    wrapper.appendChild(bubble);
    chatContainer.appendChild(wrapper);
    scrollToBottom();
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessage(message, true);
    input.value = '';
    
    // Disable input while processing
    input.disabled = true;
    sendButton.disabled = true;
    
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        removeTypingIndicator();
        
        if (data.error) {
            addMessage(`**Error:** ${data.error}`);
        } else {
            addMessage(data.response);
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('**Connection error:** Could not reach the agent server.');
        console.error(error);
    } finally {
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
});
