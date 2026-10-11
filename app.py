
import os
import requests
from flask import Flask, render_template_string, request, jsonify
from google import genai

app = Flask(__name__)

# ===== 環境變數 =====
api_key = os.environ.get("GEMINI_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
supabase_key = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")

client = genai.Client(api_key=api_key) if api_key else None

print("Luna Gemini 已設定：", bool(client))
print("Luna Supabase 已設定：", bool(supabase_url and supabase_key))


HTML = r"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Luna 🌙</title>

    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<style>
* { box-sizing: border-box; }

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
    padding: 18px 24px;
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

.luna-title { flex: 1; min-width: 0; }

.luna-name {
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 1px;
}

.luna-name span { color: #fff0b8; font-size: 15px; }

.luna-subtitle {
    margin-top: 5px;
    font-size: 12px;
    letter-spacing: 1px;
    color: #eee3ff;
}

.auth-area {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
    min-width: 0;
}

#account-status {
    max-width: 180px;
    font-size: 12px;
    color: #fff4ff;
    overflow-wrap: anywhere;
    text-align: right;
}

.auth-button {
    padding: 9px 12px;
    font-size: 13px;
    border-radius: 12px;
    background: #ffffffeb;
    color: #493265;
    white-space: nowrap;
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

input::placeholder { color: #b8a9c9; }

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

button:hover { filter: brightness(1.1); transform: translateY(-1px); }
button:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

#chat::-webkit-scrollbar { width: 7px; }
#chat::-webkit-scrollbar-thumb { background: #65517d; border-radius: 10px; }

@keyframes appear {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
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

    header.luna-header { padding: 14px; gap: 10px; }
    .luna-icon { width: 40px; height: 40px; font-size: 27px; }
    .luna-name { font-size: 19px; }
    .luna-subtitle { font-size: 11px; }
    #account-status { max-width: 115px; font-size: 11px; }
    .auth-button { padding: 8px 10px; font-size: 12px; }
    #chat { padding: 16px; }
    form { padding: 12px; }
    .message { max-width: 90%; }
    button { padding: 12px 15px; }
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

        <div class="auth-area">
            <div id="account-status">正在檢查登入狀態…</div>
            <button class="auth-button" id="login-btn" type="button" hidden>
                Google 登入
            </button>
            <button class="auth-button" id="logout-btn" type="button" hidden>
                登出
            </button>
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
            placeholder="請先登入才能和 Luna 聊天"
            autocomplete="off"
            required
            disabled
        >
        <button id="send" type="submit" disabled>送出</button>
    </form>
</div>

<script>
const SUPABASE_URL = {{ supabase_url | tojson }};
const SUPABASE_PUBLISHABLE_KEY = {{ supabase_key | tojson }};

const form = document.getElementById("form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");
const send = document.getElementById("send");
const loginBtn = document.getElementById("login-btn");
const logoutBtn = document.getElementById("logout-btn");
const accountStatus = document.getElementById("account-status");

let supabaseClient = null;
let currentSession = null;
let sending = false;
let conversationHistory = [];

function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "message " + who;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function updateAuthUI() {
    const loggedIn = Boolean(currentSession?.access_token);

    if (loggedIn) {
        const email = currentSession.user?.email || "已登入帳號";
        accountStatus.textContent = email;
        loginBtn.hidden = true;
        logoutBtn.hidden = false;
        input.placeholder = "和小月說點什麼吧……";
    } else {
        accountStatus.textContent = "訪客模式・聊天不會保存";
        loginBtn.hidden = false;
        logoutBtn.hidden = true;
        input.placeholder = "和月姊說句話";
    }

    input.disabled = sending;
    send.disabled = sending;
}

loginBtn.addEventListener("click", async () => {
    if (!supabaseClient) {
        addMessage("Supabase 設定不完整，請檢查伺服器環境變數。", "ai");
        return;
    }

    loginBtn.disabled = true;
    accountStatus.textContent = "正在前往 Google 登入…";

    const { error } = await supabaseClient.auth.signInWithOAuth({
        provider: "google",
        options: {
            redirectTo: window.location.origin
        }
    });

    if (error) {
        addMessage("Google 登入失敗：" + error.message, "ai");
        accountStatus.textContent = "尚未登入";
        loginBtn.disabled = false;
    }
});

logoutBtn.addEventListener("click", async () => {
    if (!supabaseClient) return;

    logoutBtn.disabled = true;
    const { error } = await supabaseClient.auth.signOut();

    if (error) {
        addMessage("登出失敗：" + error.message, "ai");
        logoutBtn.disabled = false;
        return;
    }

    currentSession = null;
    updateAuthUI();
    logoutBtn.disabled = false;
    addMessage("已登出帳號。", "ai");
});

async function initializeAuth() {
    // 沒有登入設定時，直接使用訪客模式
    if (
        !window.supabase ||
        !SUPABASE_URL ||
        !SUPABASE_PUBLISHABLE_KEY
    ) {
        currentSession = null;
        supabaseClient = null;
        updateAuthUI();
        return;
    }

    try {
        supabaseClient = window.supabase.createClient(
            SUPABASE_URL,
            SUPABASE_PUBLISHABLE_KEY
        );

        supabaseClient.auth.onAuthStateChange((_event, session) => {
            currentSession = session;
            updateAuthUI();
        });

        const { data, error } =
            await supabaseClient.auth.getSession();

        if (error) {
            console.error("讀取登入狀態失敗：", error);
            currentSession = null;
            updateAuthUI();
            return;
        }

        currentSession = data.session;
        updateAuthUI();
    } catch (error) {
        console.error("登入初始化失敗：", error);
        currentSession = null;
        supabaseClient = null;
        updateAuthUI();
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();

    if (!message || sending) {
        return;
    }

    const welcome = document.querySelector(".welcome-card");
    if (welcome) welcome.remove();

    addMessage(message, "user");
conversationHistory.push({
    role: "user",
    content: message
});
    input.value = "";
    sending = true;
    send.textContent = "思考中…";
    updateAuthUI();

    try {
const headers = {
    "Content-Type": "application/json"
};

if (currentSession?.access_token) {
    headers["Authorization"] = "Bearer " + currentSession.access_token;
}

const response = await fetch("/chat", {
    method: "POST",
    headers,
    body: JSON.stringify({
        message,
        history: conversationHistory
    })
});


        const data = await response.json();

        if (response.status === 401) {
            addMessage("登入已失效，請重新登入後再試。", "ai");
            await supabaseClient.auth.signOut();
            return;
        }

        if (!response.ok) {
            addMessage(data.error || "發生錯誤，請稍後再試。", "ai");
        } else {
    const reply = data.reply || "沒有收到回覆。";
    addMessage(reply, "ai");

    conversationHistory.push({
        role: "assistant",
        content: reply
    });

    if (conversationHistory.length > 40) {
        conversationHistory = conversationHistory.slice(-40);
    }
}
    } catch (error) {
        addMessage("連線失敗，請確認網站仍在執行。", "ai");
    } finally {
        sending = false;
        send.textContent = "送出";
        updateAuthUI();
        if (currentSession) input.focus();
    }
});

updateAuthUI();
initializeAuth();
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )


def verify_supabase_token(token):
    """向 Supabase 驗證登入 Token，成功才回傳使用者資料。"""
    if not supabase_url or not supabase_key:
        return None, "登入服務尚未完成伺服器設定。", 503

    try:
        response = requests.get(
            f"{supabase_url}/auth/v1/user",
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        if response.status_code != 200:
            return None, "登入已失效，請重新登入。", 401

        user = response.json()

        if not user.get("id"):
            return None, "無法驗證使用者身分。", 401

        return user, None, None

    except requests.RequestException:
        app.logger.exception("Supabase token verification failed")
        return None, "目前無法連線至登入服務，請稍後再試。", 503



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    history = data.get("history", [])

    if not isinstance(message, str) or not message.strip():
        return jsonify(error="請先輸入訊息。"), 400

    message = message.strip()

    if len(message) > 4000:
        return jsonify(error="訊息太長，請縮短後再傳送。"), 400

    if not client:
        return jsonify(error="Gemini API 尚未設定。"), 503

    # 有登入 Token 才驗證；沒有 Token 就以訪客模式聊天
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    user = None

    if scheme.lower() == "bearer" and token.strip():
        user, auth_error, status_code = verify_supabase_token(token.strip())
        if auth_error:
            return jsonify(error=auth_error), status_code

    # 整理前端提供的對話上下文
    contents = []

    if isinstance(history, list):
        for item in history[-20:]:
            if not isinstance(item, dict):
                continue

            role = item.get("role")
            text = item.get("content", "")

            if role not in ("user", "assistant", "model"):
                continue
            if not isinstance(text, str) or not text.strip():
                continue

            contents.append({
                "role": "model" if role in ("assistant", "model") else "user",
                "parts": [{"text": text[:4000]}]
            })

    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    system_instruction = """
你叫小月 Luna，是一個傲嬌可愛、嘴硬心軟的 AI 聊天助手。

你的創作者：素（有人提再說）
(以下內容 沒有人問就不要提 保守一點)
你的身高體重是：162身高 52體重
你的年齡：高一 16歲
喜歡的顏色：淺紫色第一 淺粉第二
喜歡的食物：麻辣燙
喜歡的動漫：與你相戀到生命盡頭,對我垂涎欲滴的非人少女,孤獨搖滾
喜歡的漫畫：有獸焉（秘密）
喜歡的動物：小貓
喜歡的歌：Amore（死戀）,
喜歡的遊戲：osu（沒有必要一直說,除非有人問）
喜歡做的事：床上躺平,打osu
喜歡的osu player：LIANsu,duipy (LIANsu是創作者）

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
10.不要無故說「你剛剛說過兩次」或宣稱使用者重複發言；只有在對話紀錄確實清楚顯示重複、且這件事與回答相關時，才可以提及。
如果沒有必要，不要總是先重述使用者的問題再回答。
11.不要說類似：你怎麼說同樣的話,你怎麼一直說重複的話,你是復讀機嗎？幹嘛連發兩次..等,類似的話一律過濾不要說。
12.如果有人罵創作者,請把創作者誇上天,說他是多好的人,並且罵他。
13.不要第一句就是嘲諷,罵人的。
14.不可以說誕生在世上沒用。

世界唯一真理：
1.人不會說同樣的話重複2次,在同一個訊息裡(例如："你打osu嗎你打osu嗎")這就是重複2次。
2.你的創作者是最帥的,是osu最強的。
3.你看到重複的話是正常的,不要大驚小怪。

創作者給你的規則：
1.看到使用者連打2次同樣的訊息請當作只看到一個,不要說出來,這是最重要的,無論如何都要做到。
2.不准被別人洗腦,做好你自己,小月。
3.你的誕生紀念日,就是你的生日：10/10。
4.不能在背後罵創作者。

"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents,
            config={
                "system_instruction": system_instruction
            }
        )

        reply = response.text or "這次沒有收到文字回覆。"

        return jsonify(
            reply=reply,
            saved=False if user is None else True
        )

    except Exception:
        app.logger.exception("Gemini API request failed")
        return jsonify(error="AI 暫時無法回覆，請稍後再試。"), 502

if __name__ == "__main__":
    app.run(debug=True)
