// 결과 해석 보기 버튼을 누르면 블러가 해제되고 진단 결과가 표시됩니다.
document.getElementById('show-result-button').addEventListener('click', function() {
    // 블러 처리된 내용 해제
    const chatMessages = document.querySelectorAll('.blur-content');
    chatMessages.forEach(msg => {
        msg.classList.remove('blur-content');
    });

    // 버튼을 채팅 입력 창으로 변경
    document.getElementById('chat-input-container').innerHTML = `
        <input type="text" id="chat-input" placeholder="메시지를 입력하세요..." />
        <button id="send-button">전송</button>
    `;

    // 채팅 입력 및 전송 버튼 이벤트 등록
    document.getElementById('send-button').addEventListener('click', function() {
        const chatInput = document.getElementById('chat-input');
        const message = chatInput.value.trim();

        if (message) {
            addChatMessage('user', message);
            chatInput.value = ''; // 입력창 초기화

            // 예시 응답 (실제 로직을 구현할 수 있습니다)
            setTimeout(() => {
                addChatMessage('bot', '채팅 응답 메시지입니다.');
            }, 500);
        }
    });
});

function addChatMessage(sender, message) {
    const chatOutput = document.getElementById('chat-output');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.innerText = message.trim();
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight; // 스크롤을 가장 아래로 이동
}
