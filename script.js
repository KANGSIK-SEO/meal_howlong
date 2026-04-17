document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const mealImage = document.getElementById('mealImage').files[0];

    if (!age || !gender || !mealImage) {
        alert('모든 필드를 입력해주세요.');
        return;
    }

    // 간단한 계산 로직: 기본 수명 80세, 식사 사진에 따라 랜덤 변동
    let baseLifespan = 80;
    const adjustment = Math.floor(Math.random() * 21) - 10; // -10 to +10
    const predictedLifespan = baseLifespan + adjustment;

    // 결과 표시
    const resultDiv = document.getElementById('result');
    const predictionText = document.getElementById('predictionText');
    predictionText.textContent = `당신은 ${predictedLifespan}살까지 살아있을 예정입니다.`;
    resultDiv.classList.remove('hidden');
});