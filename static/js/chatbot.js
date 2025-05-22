// advanced/static/js/chatbot.js
function toggleChatbot() {
    const chatWindow = document.getElementById("chatbotWindow");
    chatWindow.classList.toggle("open");
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("chatbotToggleBtn");
    if (btn) {
      btn.addEventListener("click", toggleChatbot);
    }
  });