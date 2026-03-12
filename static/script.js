const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const statusText = document.getElementById("status-text");

function appendMessage(role, text, isLoading = false) {
    const article = document.createElement("article");
    article.className = `message ${role}-message${isLoading ? " loading-message" : ""}`;

    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.textContent = role === "user" ? "You" : "Support Bot";

    const content = document.createElement("p");
    content.textContent = text;

    article.appendChild(meta);
    article.appendChild(content);
    chatMessages.appendChild(article);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return article;
}

function setStatus(message, isError = false) {
    statusText.textContent = message;
    statusText.classList.toggle("error", isError);
}

async function sendMessage(message) {
    const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong. Please try again.");
    }

    return data.reply;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();
    if (!message) {
        setStatus("Please enter a message before sending.", true);
        return;
    }

    appendMessage("user", message);
    messageInput.value = "";
    messageInput.focus();
    setStatus("Waiting for AI response...");
    sendButton.disabled = true;

    const loadingBubble = appendMessage("bot", "Typing...", true);

    try {
        const reply = await sendMessage(message);
        loadingBubble.remove();
        appendMessage("bot", reply);
        setStatus("Response received.");
    } catch (error) {
        loadingBubble.remove();
        appendMessage(
            "bot",
            "I could not process that right now. Your request can be forwarded to human support."
        );
        setStatus(error.message, true);
    } finally {
        sendButton.disabled = false;
    }
});
