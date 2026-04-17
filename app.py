from flask import Flask, request, jsonify, render_template
import anthropic
import base64
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.form.get("api_key", "").strip()
    age = request.form.get("age", "").strip()
    gender = request.form.get("gender", "").strip()
    image_file = request.files.get("image")

    if not api_key:
        return jsonify({"error": "API 키를 입력해주세요."}), 400
    if not image_file:
        return jsonify({"error": "사진을 업로드해주세요."}), 400

    image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
    media_type = image_file.content_type or "image/jpeg"

    gender_text = "남성" if gender == "male" else "여성" if gender == "female" else "사람"
    age_text = f"{age}세 " if age else ""

    prompt = f"""당신은 재미있는 수명 예측 AI입니다. 지금 {age_text}{gender_text}의 밥상 사진을 보고 있습니다.

밥상에 있는 음식들을 분석하여, 이 식사 습관으로는 몇 살까지 살 수 있을지 예측해주세요.

응답 형식:
1. 첫 줄: "당신은 **XX살**까지 살아있을 예정입니다! 🎉" (XX는 구체적인 숫자)
2. 두 번째 줄: 빈 줄
3. 이후: 밥상에서 발견한 식재료/음식들과 그 건강 영향 분석 (3~5줄)
4. 마지막: 건강 조언 한 마디

재미있고 유쾌하게, 하지만 영양학적으로 그럴듯하게 답해주세요. 반드시 한국어로 답하세요."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return jsonify({"result": message.content[0].text})
    except anthropic.AuthenticationError:
        return jsonify({"error": "API 키가 올바르지 않습니다."}), 401
    except Exception as e:
        return jsonify({"error": f"오류가 발생했습니다: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
