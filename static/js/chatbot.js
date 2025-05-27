function toggleChatbot() {
  const chatWindow = document.getElementById("chatbotWindow");
  chatWindow.classList.toggle("open");
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("chatbotToggleBtn")?.addEventListener("click", toggleChatbot);
  document.getElementById("chatSendBtn")?.addEventListener("click", submitMessage);
  document.getElementById("chatInput")?.addEventListener("keydown", function (e) {
    if (e.key === "Enter") submitMessage();
  });
});

async function submitMessage() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  if (!message) return;

  const chatArea = document.getElementById("chatArea");
  chatArea.innerHTML += `<div class="chat-message user">🙋 ${message}</div>`;
  input.value = "";

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();
  chatArea.innerHTML += `<div class="chat-message bot">🤖 ${data.answer}</div>`;
  chatArea.scrollTop = chatArea.scrollHeight;
}



