// advanced/static/js/chatbot.js

// 연결 확인용 로그
console.log("chatbot.js 연결됨");

// 챗봇 열기/닫기
function toggleChatbot() {
  const chatbotWindow = document.getElementById("chatbotWindow");
  chatbotWindow.classList.toggle("open");
}

document.addEventListener("DOMContentLoaded", function () {
  const chatbotToggle = document.getElementById("chatbotToggleBtn");
  chatbotToggle.addEventListener("click", toggleChatbot);

  const input = document.querySelector(".chatbot-input");
  const body = document.querySelector(".chatbot-body");

  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && input.value.trim() !== "") {
      const userMessage = input.value.trim();
      // 확인용
      console.log("사용자 질문 전송됨:", userMessage); 

      // 사용자 메시지 출력
      body.innerHTML += `<div class="chat-message chat-user">${userMessage}</div>`;

      // 로딩 중 메시지 표시
      const loadingId = `loading-${Date.now()}`;
      body.innerHTML += `<div id="${loadingId}" class="chat-message chat-bot">⏳ 답변을 생성 중입니다...</div>`;
      body.scrollTop = body.scrollHeight;
      input.value = "";

      // 서버로 전송
      fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById(loadingId).remove();

        if (data.response) {
          // 📦 디버깅용 응답 로그
          console.log("📦 응답 데이터:", data);

          let answerHtml = `<div class="chat-message chat-bot">${data.response.replace(/\n/g, "<br>")}`;

          if (data.sources && data.sources.length > 0) {
            const links = data.sources.map(src => {
              const parts = src.url.split("/");
              const pageName = parts[parts.length - 1]; // ⬅️ 여기서 pageName 정의!
              return `<a href="${src.url}" target="_blank" class="chat-source-link">📎 ${pageName}</a>`;
            }).join("<br>");;
            answerHtml += `<br><br>${links}`;
          }

          answerHtml += `</div>`;
          body.innerHTML += answerHtml;
        } else if (data.error) {
          body.innerHTML += `<div class="chat-message chat-bot error">⚠️ 오류: ${data.error}</div>`;
        }

        body.scrollTop = body.scrollHeight;
      })
      .catch(err => {
        console.error("🚨 네트워크 오류:", err); // 콘솔창에 에러 로그 출력
        body.innerHTML += `<div class="chat-message chat-bot error">⚠️ 네트워크 오류: ${err.message}</div>`;
      });

    }
  });
});
