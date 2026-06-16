document.addEventListener("DOMContentLoaded",()=>{
    const form = document.querySelector("form");
    if(form) form.addEventListener("submit",(e)=>{ e.preventDefault(); alert("Mensaje enviado. Un ejecutivo contactará pronto."); form.reset(); });
    
    // Iniciar Session ID para el CRM
    if (!localStorage.getItem("axyntrax_session_id")) {
        localStorage.setItem("axyntrax_session_id", "web_" + Math.random().toString(36).substr(2, 9));
    }
});

// Lógica del Chat Widget (PHOENIX)
function toggleChat() {
    const body = document.getElementById("ai-chat-body");
    const icon = document.getElementById("ai-chat-toggle-icon");
    if (body.style.display === "none") {
        body.style.display = "flex";
        icon.innerText = "▼";
    } else {
        body.style.display = "none";
        icon.innerText = "▲";
    }
}

function handleChatKeyPress(event) {
    if (event.key === "Enter") {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const inputField = document.getElementById("ai-chat-input");
    const message = inputField.value.trim();
    if (!message) return;
    
    appendMessage(message, "user-msg");
    inputField.value = "";
    
    const sessionId = localStorage.getItem("axyntrax_session_id");
    
    // Añadir mensaje de "pensando"
    const typingId = "typing-" + Date.now();
    appendMessage("...", "ai-msg", typingId);
    
    try {
        const response = await fetch("https://jarvis-ax-cloud-production.up.railway.app/tasks/webchat/send", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        const data = await response.json();
        document.getElementById(typingId).remove();
        
        if (data.reply) {
            appendMessage(data.reply, "ai-msg");
        } else {
            appendMessage("Ocurrió un error. Intenta nuevamente.", "ai-msg");
        }
    } catch (error) {
        document.getElementById(typingId).remove();
        appendMessage("Error de conexión. Nuestros sistemas están ocupados.", "ai-msg");
    }
}

function appendMessage(text, className, id = null) {
    const messagesContainer = document.getElementById("ai-chat-messages");
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-msg ${className}`;
    if (id) msgDiv.id = id;
    
    // Reemplazar saltos de línea por <br> para formatear la respuesta del bot
    msgDiv.innerHTML = text.replace(/\n/g, '<br>');
    
    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
