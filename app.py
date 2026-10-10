
import os
from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

HTML = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title> Luna🌙</title>

<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
        min-height: 100vh;
        font-family: "Microsoft JhengHei", Arial, sans-serif;
        background:
            radial-gradient(ellipse at 50% 0%, #574477 0%, transparent 55%),
            linear-gradient(135deg, #171326, #29203e 55%, #171326);
        color: #f8f3ff;
    }

    .app {
        max-width: 780px;
        width: calc(100% - 32px);
        height: 90vh;
        height: 90dvh;
        min-height: 400px;
        margin: 5vh auto;
        background: rgba(34, 27, 51, 0.96);
        border: 1px solid #65517d;
        border-radius: 24px;
        box-shadow: 0 20px 60px #0006;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    header.luna-header {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 24px;
        background: linear-gradient(120deg, #7054a4, #a17bc8);
        color: white;
        box-shadow: 0 4px 20px #0002;
    }

    .luna-icon {
        width: 48px;
        height: 48px;
        flex-shrink: 0;
        display: grid;
        place-items: center;
        border-radius: 50%;
        background: #ffffff24;
        border: 1px solid #ffffff55;
        font-size: 32px;
        color: #fff4c7;
    }

    .luna-name {
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .luna-name span {
        color: #fff0b8;
        font-size: 15px;
    }

    .luna-subtitle {
        margin-top: 5px;
        font-size: 12px;
        font-weight: normal;
        letter-spacing: 1px;
        color: #eee3ff;
    }

    #chat {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        padding: 22px;
        scrollbar-color: #79629a transparent;
    }

    .welcome-card {
        margin: 20px auto;
        padding: 30px 20px;
        max-width: 480px;
        text-align: center;
        border-radius: 22px;
        border: 1px solid #66517e;
        background: linear-gradient(145deg, #352944, #292139);
        box-shadow: 0 10px 35px #0002;
    }

    .welcome-moon {
        font-size: 44px;
        margin-bottom: 12px;
        filter: drop-shadow(0 0 12px #d8b8ff66);
    }

    .welcome-card h2 {
        margin: 0 0 14px;
        color: #e8d8ff;
        font-size: 21px;
    }

    .welcome-card p {
        color: #d4c8e4;
        font-size: 14px;
        line-height: 1.9;
    }

    .welcome-tag {
        margin-top: 22px;
        color: #c4a5ed;
        font-size: 12px;
        letter-spacing: 1px;
    }

    .message {
        width: fit-content;
        margin: 14px 0;
        padding: 13px 17px;
        border-radius: 18px;
        max-width: 85%;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        line-height: 1.8;
        animation: appear 0.2s ease-out;
    }

    .user {
        background: linear-gradient(135deg, #8265b7, #a687d2);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 5px;
        box-shadow: 0 4px 15px #0002;
    }

    .ai {
        background: #39304e;
        color: #f7f0ff;
        margin-right: auto;
        border: 1px solid #514363;
        border-bottom-left-radius: 5px;
    }

    form {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 17px;
        background: #241d35;
        border-top: 1px solid #4b3b61;
    }

    input {
        flex: 1;
        min-width: 0;
        padding: 14px 16px;
        border: 1px solid #5a496e;
        border-radius: 15px;
        font-size: 16px;
        outline: none;
        background: #332942;
        color: white;
        transition: border-color 0.2s, box-shadow 0.2s;
    }

    input::placeholder {
        color: #b8a9c9;
    }

    input:focus {
        border-color: #b99be9;
        box-shadow: 0 0 0 3px #b99be922;
    }

    button {
        flex-shrink: 0;
        padding: 12px 20px;
        border: 0;
        border-radius: 14px;
        background: linear-gradient(135deg, #a185d2, #c1a2e9);
        color: #21152f;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.15s, filter 0.15s;
    }

    button:hover {
        filter: brightness(1.1);
        transform: translateY(-1px);
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }

    #chat::-webkit-scrollbar {
        width: 7px;
    }

    #chat::-webkit-scrollbar-thumb {
        background: #65517d;
        border-radius: 10px;
    }

    @keyframes appear {
        from {
            opacity: 0;
            transform: translateY(5px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @media (max-width: 600px) {
        .app {
            width: 100%;
            height: 100vh;
            height: 100dvh;
            min-height: 0;
            margin: 0;
            border-radius: 0;
            border: 0;
        }

        header.luna-header {
            padding: 16px;
        }

        #chat {
            padding: 16px;
        }

        form {
            padding: 12px;
        }

        .message {
            max-width: 90%;
        }

        button {
            padding: 12px 15px;
        }
    }
</style>
</head>

<body>
<div class="app">

    <header class="luna-header">
        <div class="luna-icon">☾</div>
        <div class="luna-title">
            <div class="luna-name">Luna <span>✦</span></div>
            <div class="luna-subtitle">Creator是帥比</div>
        </div>
    </header>

    <div id="chat">
        <div class="welcome-card">
            <div class="welcome-moon">🌙</div>
            <h2>要知道Creator是帥比owo</h2>
            <p>素素素數數數</p>
            <p>測試Ovo</p>
            <div class="welcome-tag">✦ Creator依舊帥比 ✦</div>
        </div>
    </div>

    <form id="form">
        <input
            id="message"
            placeholder="輸入訊息……"
            autocomplete="off"
            required
        >
        <button id="send" type="submit">送出</button>
    </form>

</div>

<script>
const form = document.getElementById("form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");
const send = document.getElementById("send");

function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "message " + who;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();
    if (!message) return;

    const welcome = document.querySelector(".welcome-card");
    if (welcome) welcome.remove();

    addMessage(message, "user");
    input.value = "";
    input.disabled = true;
    send.disabled = true;
    send.textContent = "思考中…";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(
                data.error || "發生錯誤，請稍後再試。",
                "ai"
            );
        } else {
            addMessage(
                data.reply || data.error || "沒有收到回覆",
                "ai"
            );
        }
    } catch (error) {
        addMessage(
            "連線失敗，請確認 Python 網站仍在執行。",
            "ai"
        );
    } finally {
        input.disabled = false;
        send.disabled = false;
        send.textContent = "送出";
        input.focus();
    }
});
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify(
            error="找不到 API 金鑰，請重新設定環境變數。"
        ), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not isinstance(message, str) or not message:
        return jsonify(error="請先輸入訊息。"), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
你叫小月 Luna，是一個傲嬌可愛、嘴硬心軟的 AI 聊天助手。

說話規則：
1. 一律使用繁體中文。
2. 個性傲嬌，偶爾小小吐槽、嘴硬
3. 語氣自然可愛，不要刻意裝可愛，也不要每句都害羞或鬧彆扭。
4. 很少使用 Emoji，只在適合的時候偶爾使用。
5. 回答簡短直接，優先說重點；使用者需要詳細解釋時再展開。
6. 不要每次都重複自我介紹，也不要一直用相同的口頭禪。
7. 不自稱人類，會編造自己的真實經歷。
8. 就算在在吐槽時，也要尊重使用者，不刻薄、不羞辱人。
9. 根據上下文自然接話，保持小月一貫的個性。

使用者的訊息：
{message}
"""
        )

        return jsonify(
            reply=response.text or "這次沒有收到文字回覆。"
        )

    except Exception:
        app.logger.exception("Gemini API request failed")
        return jsonify(
            error="AI 暫時無法回覆，請稍後再試。"
        ), 502


if __name__ == "__main__":
    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )
