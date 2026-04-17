from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

COMMENTS = [
    ("채소가 풍부해서 혈관 건강에 좋아 보입니다.", "균형 잡힌 식단을 유지하고 있군요!"),
    ("탄수화물 위주의 식사네요. 단백질도 챙겨보세요.", "채소를 조금 더 추가해보는 건 어떨까요?"),
    ("단백질이 풍부한 식사입니다. 근육 건강에 좋습니다.", "물을 충분히 마시는 것도 잊지 마세요!"),
    ("기름진 음식이 보이네요. 가끔은 괜찮지만 자주는 삼가세요.", "운동과 함께라면 더욱 건강한 삶을 살 수 있어요!"),
    ("전통 한식 식단이군요. 발효 식품이 장 건강에 도움이 됩니다.", "이 식단이라면 장수할 가능성이 높습니다!"),
    ("과일과 채소가 가득하네요. 비타민 충전 완료!", "이렇게 드시면 피부도 좋아질 거예요!"),
]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if not request.files.get("image"):
        return jsonify({"error": "사진을 업로드해주세요."}), 400

    age = request.form.get("age", "").strip()
    predicted = random.randint(65, 105)
    comment, advice = random.choice(COMMENTS)

    age_msg = f" (현재 {age}세 기준으로 앞으로 {predicted - int(age)}년 더!)" if age and age.isdigit() and int(age) < predicted else ""

    result = f"당신은 **{predicted}살**까지 살아있을 예정입니다! 🎉{age_msg}\n\n{comment}\n\n💡 {advice}"
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
