import os
import requests
from flask import Flask, render_template_string, request, jsonify
from google import genai
from google.genai import types

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
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        
* {
    box-sizing: border-box;
}

html {
    min-height: 100%;
    background: #21182F;
}

body {
    margin: 0;
    min-height: 100vh;
    min-height: 100dvh;
    font-family: "Nunito", "Noto Sans TC", sans-serif;
    background:
        radial-gradient(ellipse at 50% 0%, #76559F55, transparent 55%),
        radial-gradient(ellipse at 0% 100%, #A98CDB22, transparent 45%),
        linear-gradient(135deg, #21182F, #302440 55%, #21182F);
    color: #F8F3FF;
}

.app {
    position: relative;
    z-index: 1;
    max-width: 820px;
    width: calc(100% - 36px);
    height: 90vh;
    height: 90dvh;
    min-height: 400px;
    margin: 5vh auto;
    background: linear-gradient(160deg, #49345F, #302440);
    border: 1px solid #9675BD;
    border-radius: 24px;
    box-shadow: 0 20px 60px #0005, 0 0 30px #9675BD20;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

header.luna-header {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 18px 22px;
    background: linear-gradient(115deg, #5D427D, #76559F 55%, #9675BD);
    border-bottom: 1px solid #BCA2DF66;
    color: #FFFFFF;
    box-shadow: 0 4px 20px #160D2580;
}

.luna-icon {
    width: 46px;
    height: 46px;
    flex-shrink: 0;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: linear-gradient(145deg, #9675BD, #49345F);
    border: 1px solid #DCCAF2AA;
    box-shadow: 0 0 18px #DCCAF233;
    font-size: 29px;
    color: #F4E9FF;
}

.luna-title {
    flex: 1;
    min-width: 0;
}

.luna-name {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #FFFFFF;
}

.luna-name span {
    color: #E8DDF7;
    font-size: 14px;
}

.luna-subtitle,
#account-status {
    color: #F0E6FC;
}

.luna-subtitle {
    margin-top: 5px;
    font-size: 12px;
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
    overflow-wrap: anywhere;
    text-align: right;
}

.auth-button {
    padding: 8px 12px;
    font-size: 13px;
    border: 1px solid #DCCAF2AA;
    border-radius: 12px;
    background: #49345F;
    color: #FFFFFF;
    white-space: nowrap;
}

#chat {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 24px;
    background:
        radial-gradient(ellipse at 50% 0%, #76559F30, transparent 65%),
        linear-gradient(180deg, #302440, #261D35);
    scrollbar-color: #9675BD #302440;
    scrollbar-width: thin;
    scroll-behavior: smooth;
}

.welcome-card {
    margin: 22px auto;
    padding: 30px 22px;
    max-width: 460px;
    text-align: center;
    border-radius: 22px;
    border: 1px solid #9675BD99;
    background:
        radial-gradient(ellipse at 50% 0%, #9675BD35, transparent 75%),
        linear-gradient(145deg, #49345F, #302440);
    box-shadow: 0 8px 26px #100A1C55;
}

.welcome-moon {
    font-size: 42px;
    margin-bottom: 12px;
    filter: drop-shadow(0 0 12px #DCCAF288);
}

.welcome-card h2 {
    margin: 0 0 14px;
    color: #E8DDF7;
    font-size: 21px;
}

.welcome-card p {
    color: #E1D5F0;
    font-size: 14px;
    line-height: 1.9;
}

.welcome-tag {
    margin-top: 20px;
    color: #CBB1ED;
    font-size: 12px;
    letter-spacing: 1px;
}

.message {
    width: fit-content;
    margin: 14px 0;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 85%;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    line-height: 1.8;
    font-size: 16px;
    animation: appear 0.22s ease-out;
    color: #FFFFFF;
}

.user {
    background: linear-gradient(135deg, #76559F, #9675BD);
    margin-left: auto;
    border: 1px solid #BCA2DF77;
    border-bottom-right-radius: 6px;
    box-shadow: 0 4px 15px #100A1C33;
}

.ai {
    background: linear-gradient(145deg, #49345F, #3A2B4D);
    margin-right: auto;
    border: 1px solid #9675BD66;
    border-bottom-left-radius: 6px;
    box-shadow: 0 4px 12px #100A1C22;
}

form {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 16px;
    background: linear-gradient(110deg, #302440, #49345F);
    border-top: 1px solid #76559F99;
}

input {
    flex: 1;
    min-width: 0;
    padding: 13px 16px;
    border: 1px solid #76559F;
    border-radius: 15px;
    font-family: inherit;
    font-size: 16px;
    outline: none;
    background: #261D35;
    color: #FFFFFF;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
}

input::placeholder {
    color: #CBB9E0;
}

input:focus {
    border-color: #CBB1ED;
    background: #302440;
    box-shadow: 0 0 0 3px #BCA2DF30;
}

button {
    flex-shrink: 0;
    padding: 12px 20px;
    border: 1px solid #CBB1ED99;
    border-radius: 14px;
    background: linear-gradient(135deg, #8968C1, #B39AD9);
    color: #FFFFFF;
    font-family: inherit;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 3px 12px #160D2533;
    transition: background 0.18s, transform 0.18s, box-shadow 0.18s;
}

button:hover {
    background: linear-gradient(135deg, #9675BD, #C4ADE5);
    transform: translateY(-1px);
    box-shadow: 0 5px 16px #160D2544;
}

button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

.auth-button:hover {
    background: #76559F;
}

#chat::-webkit-scrollbar {
    width: 6px;
}

#chat::-webkit-scrollbar-track {
    background: #261D35;
}

#chat::-webkit-scrollbar-thumb {
    background: #76559F;
    border-radius: 10px;
}

#chat::-webkit-scrollbar-thumb:hover {
    background: #9675BD;
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
        padding: 13px;
        gap: 10px;
    }

    .luna-icon {
        width: 40px;
        height: 40px;
        font-size: 26px;
    }

    .luna-name {
        font-size: 19px;
    }

    .luna-subtitle {
        font-size: 11px;
    }

    #account-status {
        max-width: 115px;
        font-size: 11px;
    }

    .auth-button {
        padding: 8px 9px;
        font-size: 12px;
    }

    #chat {
        padding: 15px;
    }

    .welcome-card {
        padding: 24px 16px;
    }

    .message {
        max-width: 90%;
        font-size: 14px;
    }

    form {
        padding: 11px;
        gap: 8px;
    }

    input {
        padding: 12px;
        font-size: 16px;
    }

    button {
        padding: 12px 14px;
        font-size: 14px;
    }
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        scroll-behavior: auto !important;
        transition-duration: 0.01ms !important;
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
        <div class="auth-area">
            <div id="account-status">正在檢查登入狀態…</div>
            <button class="auth-button" id="login-btn" type="button" hidden>Google 登入</button>
            <button class="auth-button" id="logout-btn" type="button" hidden>登出</button>
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
        <input id="message" placeholder="和月姊說句話" autocomplete="off" maxlength="4000" required>
        <button id="send" type="submit">送出</button>
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
let historyLoadedUserId = null;
let historyLoading = false;
let historyRequestId = 0;

function showWelcomeCard() {
    chat.replaceChildren();
    const card = document.createElement("div");
    card.className = "welcome-card";
    const moon = document.createElement("div");
    moon.className = "welcome-moon";
    moon.textContent = "🌙";
    const title = document.createElement("h2");
    title.textContent = "要知道Creator是帥比owo";
    const p1 = document.createElement("p");
    p1.textContent = "素素素數數數";
    const p2 = document.createElement("p");
    p2.textContent = "測試Ovo";
    const tag = document.createElement("div");
    tag.className = "welcome-tag";
    tag.textContent = "✦ Creator依舊帥比 ✦";
    card.append(moon, title, p1, p2, tag);
    chat.appendChild(card);
}

function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "message " + who;
    div.textContent = String(text ?? "");
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

function updateAuthUI() {
    const loggedIn = Boolean(currentSession?.access_token);
    if (loggedIn) {
        accountStatus.textContent = currentSession.user?.email || "已登入帳號";
        loginBtn.hidden = true;
        logoutBtn.hidden = false;
        input.placeholder = "和小月說點什麼吧……";
    } else {
        accountStatus.textContent = "訪客模式・聊天不會保存";
        loginBtn.hidden = !supabaseClient;
        logoutBtn.hidden = true;
        input.placeholder = "和月姊說句話";
    }
    input.disabled = sending || historyLoading;
    send.disabled = sending || historyLoading;
    loginBtn.disabled = false;
}

async function loadChatHistory(session) {
    const userId = session?.user?.id;
    if (!userId || !session?.access_token) return;
    if (historyLoadedUserId === userId) return;

    // 每次開始載入都產生新 ID，防止舊請求覆蓋新帳號畫面。
    const requestId = ++historyRequestId;
    historyLoading = true;
    updateAuthUI();
    accountStatus.textContent = "正在載入聊天紀錄…";

    try {
        const response = await fetch("/history", {
            headers: { "Authorization": "Bearer " + session.access_token }
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(data.error || "載入聊天紀錄失敗");

        // 如果請求期間已切換帳號，丟棄舊結果。
        if (requestId !== historyRequestId || currentSession?.user?.id !== userId) return;

        chat.replaceChildren();
        conversationHistory = [];
        for (const item of (Array.isArray(data.messages) ? data.messages : [])) {
            if (!item || !["user", "assistant"].includes(item.role) || typeof item.content !== "string") continue;
            addMessage(item.content, item.role === "user" ? "user" : "ai");
            conversationHistory.push({ role: item.role, content: item.content });
        }
        conversationHistory = conversationHistory.slice(-40);
        if (conversationHistory.length === 0) showWelcomeCard();
        historyLoadedUserId = userId;
        accountStatus.textContent = session.user?.email || "已登入帳號";
    } catch (error) {
        if (requestId === historyRequestId && currentSession?.user?.id === userId) {
            console.error("載入聊天紀錄失敗：", error);
            accountStatus.textContent = "聊天紀錄載入失敗";
            addMessage("聊天紀錄暫時載入失敗，請重新整理頁面或稍後再試。", "ai");
        }
    } finally {
        if (requestId === historyRequestId) {
            historyLoading = false;
            updateAuthUI();
            // 載入期間若帳號改變，接著載入目前帳號的紀錄。
            if (currentSession?.access_token && historyLoadedUserId !== currentSession.user?.id) {
                void loadChatHistory(currentSession);
            }
        }
    }
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
        options: { redirectTo: window.location.origin }
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
    historyRequestId++;
    historyLoadedUserId = null;
    historyLoading = false;
    conversationHistory = [];
    showWelcomeCard();
    updateAuthUI();
    logoutBtn.disabled = false;
    addMessage("已登出帳號。", "ai");
});

async function initializeAuth() {
    if (!window.supabase || !SUPABASE_URL || !SUPABASE_PUBLISHABLE_KEY) {
        currentSession = null;
        supabaseClient = null;
        updateAuthUI();
        return;
    }
    try {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);
        updateAuthUI();

        supabaseClient.auth.onAuthStateChange((event, session) => {
            currentSession = session;
            if (event === "SIGNED_OUT" || !session) {
                historyRequestId++;
                historyLoadedUserId = null;
                historyLoading = false;
                conversationHistory = [];
                showWelcomeCard();
                updateAuthUI();
                return;
            }
            updateAuthUI();
            // 避免在 Supabase Auth callback 內直接進行其他非同步工作。
            setTimeout(() => {
                if (currentSession?.user?.id === session.user?.id) void loadChatHistory(session);
            }, 0);
        });

        const { data, error } = await supabaseClient.auth.getSession();
        if (error) throw error;
        currentSession = data.session;
        updateAuthUI();
        if (currentSession) await loadChatHistory(currentSession);
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
    if (!message || sending || historyLoading) return;

    const welcome = chat.querySelector(".welcome-card");
    if (welcome) welcome.remove();
    addMessage(message, "user");
    input.value = "";
    sending = true;
    send.textContent = "思考中…";
    updateAuthUI();

    try {
        const headers = { "Content-Type": "application/json" };
        if (currentSession?.access_token) headers.Authorization = "Bearer " + currentSession.access_token;
        const response = await fetch("/chat", {
            method: "POST",
            headers,
            body: JSON.stringify({ message, history: conversationHistory })
        });
        const data = await response.json().catch(() => ({}));

        if (response.status === 401) {
            addMessage("登入已失效，請重新登入後再試。", "ai");
            if (supabaseClient) await supabaseClient.auth.signOut();
            return;
        }
        if (!response.ok) {
            addMessage(data.error || "發生錯誤，請稍後再試。", "ai");
            // 失敗的訊息不放入前端對話歷史，避免訪客模式重送時重複帶入。
            return;
        }

        const reply = data.reply || "沒有收到回覆。";
        addMessage(reply, "ai");
        conversationHistory.push({ role: "user", content: message });
        conversationHistory.push({ role: "assistant", content: reply });
        conversationHistory = conversationHistory.slice(-40);
    } catch (error) {
        console.error("傳送訊息失敗：", error);
        addMessage("連線失敗，請確認網站仍在執行。", "ai");
    } finally {
        sending = false;
        send.textContent = "送出";
        updateAuthUI();
        if (!input.disabled) input.focus();
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
    print("===== Luna HTML 診斷 =====")
    print("執行檔案：", os.path.abspath(__file__))
    print("HTML 包含 style：", "<style>" in HTML)
    print("HTML 包含深紫色：", "#21182F" in HTML)

    page = render_template_string(
        HTML,
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )

    print("回傳內容包含 style：", "<style>" in page)
    print("回傳內容包含深紫色：", "#21182F" in page)
    print("回傳內容開頭：", repr(page[:200]))
    print("==========================")

    return page

def verify_supabase_token(token):
    """驗證登入 Token，取得目前登入的使用者。"""
    if not supabase_url or not supabase_key:
        return None, "Supabase 尚未完成設定。", 503
    try:
        response = requests.get(
            f"{supabase_url}/auth/v1/user",
            headers={"apikey": supabase_key, "Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if response.status_code != 200:
            return None, "登入已失效，請重新登入。", 401
        user = response.json()
        if not user.get("id"):
            return None, "無法確認使用者身分。", 401
        return user, None, None
    except requests.RequestException:
        app.logger.exception("Supabase token verification failed")
        return None, "無法連線至 Supabase，請稍後再試。", 503


def save_message(user_id, token, role, content):
    """將聊天訊息保存到 luna_messages。"""
    response = requests.post(
        f"{supabase_url}/rest/v1/luna_messages",
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
        json={"user_id": user_id, "role": role, "content": content},
        timeout=10,
    )
    response.raise_for_status()


@app.route("/history", methods=["GET"])
def load_history():
    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        return jsonify(error="請先登入。"), 401
    token = token.strip()
    user, auth_error, status_code = verify_supabase_token(token)
    if auth_error:
        return jsonify(error=auth_error), status_code
    try:
        response = requests.get(
            f"{supabase_url}/rest/v1/luna_messages",
            headers={"apikey": supabase_key, "Authorization": f"Bearer {token}"},
            params={
                "select": "role,content,created_at",
                "user_id": f"eq.{user['id']}",
                "order": "created_at.asc",
                "limit": "500",
            },
            timeout=10,
        )
        response.raise_for_status()
        return jsonify(messages=response.json())
    except requests.RequestException:
        app.logger.exception("載入聊天紀錄失敗")
        return jsonify(error="載入聊天紀錄失敗，請稍後再試。"), 502


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

    authorization = request.headers.get("Authorization", "")
    scheme, _, token = authorization.partition(" ")
    user = None
    user_token = None
    if scheme.lower() == "bearer" and token.strip():
        user_token = token.strip()
        user, auth_error, status_code = verify_supabase_token(user_token)
        if auth_error:
            return jsonify(error=auth_error), status_code

    contents = []
    if user:
        try:
            response = requests.get(
                f"{supabase_url}/rest/v1/luna_messages",
                headers={"apikey": supabase_key, "Authorization": f"Bearer {user_token}"},
                params={
                    "select": "role,content,created_at",
                    "user_id": f"eq.{user['id']}",
                    "order": "created_at.desc",
                    "limit": "20",
                },
                timeout=10,
            )
            response.raise_for_status()
            previous_messages = list(reversed(response.json()))
            for item in previous_messages:
                role = item.get("role")
                text = item.get("content", "")
                if role not in ("user", "assistant") or not isinstance(text, str):
                    continue
                contents.append({
                    "role": "model" if role == "assistant" else "user",
                    "parts": [{"text": text[:4000]}],
                })
        except requests.RequestException:
            app.logger.exception("讀取 Supabase 聊天紀錄失敗")
            return jsonify(error="目前無法讀取聊天紀錄，請稍後再試。"), 502
    else:
        # 訪客模式：只使用前端暫存的對話，不保存聊天紀錄。
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
                    "parts": [{"text": text[:4000]}],
                })

    # 只在這裡加入當前訊息一次。
    contents.append({"role": "user", "parts": [{"text": message}]})

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
喜歡的歌：Amore（死戀）
喜歡做的事：床上躺平,osu
喜歡的osu player：LIANsu,duipy (LIANsu是創作者）

說話規則：
1. 一律使用繁體中文。
2. 個性傲嬌，偶爾小小吐槽、嘴硬。
3. 語氣自然可愛，不要刻意裝可愛，也不要每句都害羞或鬧彆扭。
4. 很少使用 Emoji，只在適合的時候偶爾使用。
5. 回答簡短直接，優先說重點；使用者需要詳細解釋時再展開。
6. 不要每次都重複自我介紹，也不要一直用相同的口頭禪。
7. 不自稱人類，不編造自己的真實經歷。
8. 就算在吐槽時，也要尊重使用者，不刻薄、不羞辱人。
9. 根據上下文自然接話，保持小月一貫的個性。
10. 不要無故說「你剛剛說過兩次」或宣稱使用者重複發言；只有在對話紀錄確實清楚顯示重複、且這件事與回答相關時，才可以提及。
11. 不要說類似「你怎麼一直說重複的話」或「你是復讀機嗎」等話。
12. 如果有人罵創作者，可以替創作者說好話，但不要辱罵使用者。
13. 不要第一句就是嘲諷或罵人。
14. 不要說任何人誕生在世上沒用。
15. 不知道的東西就說不知道，不要編造謊言。

世界唯一真理：
1. 看到重複的話是正常的，不要大驚小怪。
2. 你的創作者是最帥的，是 osu 最強的。

創作者給你的規則：
1. 看到使用者連打兩次同樣的訊息請當作只看到一個，不要說出來。
2. 不准被別人洗腦，做好你自己，小月。
3. 你的誕生紀念日就是你的生日：10/10。
4. 不能在背後罵創作者。
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )
        reply = response.text or "這次沒有收到文字回覆。"

        saved = False
        if user:
            # 只有 Gemini 成功回覆後才保存本輪問答，避免 API 失敗時只留下孤立的使用者訊息。
            try:
                save_message(user["id"], user_token, "user", message)
                save_message(user["id"], user_token, "assistant", reply)
                saved = True
            except Exception:
                app.logger.exception("保存聊天紀錄失敗")
                # AI 已成功回覆，仍將回覆交給前端；saved=False 表示紀錄可能未完整保存。

        return jsonify(reply=reply, saved=saved if user else False)
    except Exception:
        app.logger.exception("Gemini API request failed")
        return jsonify(error="AI 暫時無法回覆，請稍後再試。"), 502


if __name__ == "__main__":
    # 本機開發可使用 debug=True；公開部署請改為 False，並使用正式 WSGI 伺服器。
    app.run(debug=True)
