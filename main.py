import os
import uuid
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

app = FastAPI()

APP_NAME = "study_guide"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# 🌐 Modern Glassmorphism UI
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Study Buddy AI</title>
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet"/>
        <style>
            *, *::before, *::after {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            :root {
                --glass-bg: rgba(255, 255, 255, 0.06);
                --glass-border: rgba(255, 255, 255, 0.12);
                --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
                --accent-1: #a78bfa;
                --accent-2: #38bdf8;
                --accent-3: #f472b6;
                --text-primary: #f1f5f9;
                --text-muted: #94a3b8;
                --input-bg: rgba(15, 23, 42, 0.6);
            }

            html, body {
                height: 100%;
                font-family: 'DM Sans', sans-serif;
                background: #050a18;
                color: var(--text-primary);
                overflow-x: hidden;
            }

            /* ── Animated mesh background ── */
            .bg-mesh {
                position: fixed;
                inset: 0;
                z-index: 0;
                overflow: hidden;
            }

            .bg-mesh::before {
                content: '';
                position: absolute;
                width: 900px; height: 900px;
                top: -200px; left: -200px;
                background: radial-gradient(circle, rgba(167,139,250,0.18) 0%, transparent 65%);
                animation: drift1 18s ease-in-out infinite alternate;
                border-radius: 50%;
            }

            .bg-mesh::after {
                content: '';
                position: absolute;
                width: 700px; height: 700px;
                bottom: -150px; right: -150px;
                background: radial-gradient(circle, rgba(56,189,248,0.15) 0%, transparent 65%);
                animation: drift2 14s ease-in-out infinite alternate;
                border-radius: 50%;
            }

            .bg-orb-3 {
                position: fixed;
                width: 500px; height: 500px;
                top: 40%; left: 50%;
                transform: translate(-50%, -50%);
                background: radial-gradient(circle, rgba(244,114,182,0.1) 0%, transparent 65%);
                border-radius: 50%;
                animation: drift3 20s ease-in-out infinite alternate;
                pointer-events: none;
                z-index: 0;
            }

            @keyframes drift1 {
                from { transform: translate(0, 0) scale(1); }
                to   { transform: translate(80px, 60px) scale(1.12); }
            }
            @keyframes drift2 {
                from { transform: translate(0, 0) scale(1); }
                to   { transform: translate(-60px, -80px) scale(1.08); }
            }
            @keyframes drift3 {
                from { transform: translate(-50%, -50%) scale(1); }
                to   { transform: translate(-45%, -55%) scale(1.15); }
            }

            /* ── Grid noise overlay ── */
            .noise {
                position: fixed;
                inset: 0;
                z-index: 1;
                opacity: 0.025;
                background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
                background-size: 200px 200px;
                pointer-events: none;
            }

            /* ── Header ── */
            header {
                position: relative;
                z-index: 10;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 18px 32px;
                background: rgba(5, 10, 24, 0.7);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--glass-border);
                animation: slideDown 0.6s ease forwards;
            }

            @keyframes slideDown {
                from { opacity: 0; transform: translateY(-20px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            .logo {
                display: flex;
                align-items: center;
                gap: 10px;
                font-family: 'Syne', sans-serif;
                font-weight: 800;
                font-size: 20px;
                letter-spacing: -0.3px;
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .logo-icon {
                width: 32px; height: 32px;
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                border-radius: 8px;
                display: flex; align-items: center; justify-content: center;
                font-size: 16px;
                animation: pulse-glow 3s ease-in-out infinite;
            }

            @keyframes pulse-glow {
                0%, 100% { box-shadow: 0 0 12px rgba(167,139,250,0.4); }
                50%       { box-shadow: 0 0 24px rgba(56,189,248,0.6); }
            }

            .header-badge {
                font-size: 11px;
                padding: 4px 12px;
                border-radius: 20px;
                background: var(--glass-bg);
                border: 1px solid var(--glass-border);
                color: var(--text-muted);
                letter-spacing: 0.5px;
                font-weight: 500;
            }

            /* ── Main layout ── */
            .container {
                position: relative;
                z-index: 5;
                max-width: 820px;
                margin: 48px auto 0;
                padding: 0 20px 40px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                animation: fadeUp 0.7s 0.2s ease both;
            }

            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(28px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            /* ── Welcome banner ── */
            .welcome-banner {
                text-align: center;
                padding: 8px 0 4px;
            }

            .welcome-banner h1 {
                font-family: 'Syne', sans-serif;
                font-size: clamp(26px, 5vw, 38px);
                font-weight: 800;
                background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 50%, var(--accent-3) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1.15;
                letter-spacing: -0.5px;
            }

            .welcome-banner p {
                color: var(--text-muted);
                font-size: 14px;
                margin-top: 8px;
                font-weight: 300;
            }

            /* ── Chat box ── */
            .chat-glass {
                background: var(--glass-bg);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid var(--glass-border);
                border-radius: 20px;
                min-height: 340px;
                padding: 28px 32px;
                box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.07);
                transition: border-color 0.3s ease;
                position: relative;
                overflow: hidden;
            }

            .chat-glass::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), rgba(56,189,248,0.4), transparent);
            }

            /* ── Message states ── */
            .msg-welcome {
                display: flex;
                align-items: flex-start;
                gap: 14px;
                animation: fadeIn 0.5s ease;
            }

            .msg-avatar {
                width: 36px; height: 36px;
                border-radius: 10px;
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                display: flex; align-items: center; justify-content: center;
                font-size: 17px;
                flex-shrink: 0;
                box-shadow: 0 4px 12px rgba(167,139,250,0.35);
            }

            .msg-content {
                flex: 1;
            }

            .msg-label {
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.8px;
                text-transform: uppercase;
                color: var(--accent-1);
                margin-bottom: 6px;
                font-family: 'Syne', sans-serif;
            }

            .msg-text {
                font-size: 15px;
                line-height: 1.7;
                color: var(--text-primary);
                font-weight: 300;
                white-space: pre-wrap;
            }

            /* ── Thinking animation ── */
            .thinking {
                display: flex;
                align-items: center;
                gap: 14px;
                animation: fadeIn 0.3s ease;
            }

            .thinking-dots {
                display: flex;
                gap: 6px;
                align-items: center;
                padding: 4px 0;
            }

            .thinking-dots span {
                width: 8px; height: 8px;
                border-radius: 50%;
                background: var(--accent-2);
                animation: bounce 1.2s ease-in-out infinite;
            }

            .thinking-dots span:nth-child(2) { animation-delay: 0.2s; background: var(--accent-1); }
            .thinking-dots span:nth-child(3) { animation-delay: 0.4s; background: var(--accent-3); }

            @keyframes bounce {
                0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
                40%            { transform: translateY(-8px); opacity: 1; }
            }

            /* ── Input area ── */
            .input-wrapper {
                background: var(--glass-bg);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid var(--glass-border);
                border-radius: 16px;
                padding: 6px 6px 6px 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255,255,255,0.07);
                transition: border-color 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }

            .input-wrapper::before {
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), rgba(56,189,248,0.3), transparent);
            }

            .input-wrapper:focus-within {
                border-color: rgba(167,139,250,0.4);
                box-shadow: var(--glass-shadow), 0 0 0 3px rgba(167,139,250,0.1), inset 0 1px 0 rgba(255,255,255,0.07);
            }

            #query {
                flex: 1;
                background: transparent;
                border: none;
                outline: none;
                font-family: 'DM Sans', sans-serif;
                font-size: 15px;
                font-weight: 400;
                color: var(--text-primary);
                padding: 10px 0;
            }

            #query::placeholder {
                color: var(--text-muted);
                font-weight: 300;
            }

            .send-btn {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 10px 20px;
                background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
                border: none;
                border-radius: 10px;
                color: #0a0a1a;
                font-family: 'Syne', sans-serif;
                font-weight: 700;
                font-size: 13px;
                letter-spacing: 0.3px;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s;
                box-shadow: 0 4px 16px rgba(167,139,250,0.35);
                flex-shrink: 0;
            }

            .send-btn:hover {
                transform: translateY(-1px) scale(1.02);
                box-shadow: 0 6px 24px rgba(167,139,250,0.5);
            }

            .send-btn:active {
                transform: scale(0.97);
            }

            .send-btn:disabled {
                opacity: 0.55;
                cursor: not-allowed;
                transform: none;
            }

            .send-btn svg {
                width: 14px; height: 14px;
                transition: transform 0.2s ease;
            }

            .send-btn:hover svg {
                transform: translateX(2px);
            }

            /* ── Hint chips ── */
            .hint-chips {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                justify-content: center;
                animation: fadeUp 0.7s 0.5s ease both;
            }

            .chip {
                font-size: 12px;
                padding: 6px 14px;
                border-radius: 20px;
                background: var(--glass-bg);
                border: 1px solid var(--glass-border);
                color: var(--text-muted);
                cursor: pointer;
                transition: all 0.2s ease;
                white-space: nowrap;
                font-weight: 400;
            }

            .chip:hover {
                border-color: rgba(167,139,250,0.4);
                color: var(--accent-1);
                background: rgba(167,139,250,0.08);
                transform: translateY(-1px);
            }

            /* ── Response text formatting ── */
            .msg-text strong, .msg-text b {
                color: var(--accent-2);
                font-weight: 600;
            }

            .msg-text em, .msg-text i {
                color: var(--accent-3);
            }

            /* ── Utility ── */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            ::-webkit-scrollbar { width: 5px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 4px; }

            @media (max-width: 600px) {
                .container { margin-top: 28px; }
                .chat-glass { padding: 20px; }
                header { padding: 14px 20px; }
            }
        </style>
    </head>
    <body>

        <div class="bg-mesh"></div>
        <div class="bg-orb-3"></div>
        <div class="noise"></div>

        <header>
            <div class="logo">
                <div class="logo-icon">📘</div>
                Study Buddy
            </div>
            <div class="header-badge">AI · Powered</div>
        </header>

        <div class="container">

            <div class="welcome-banner">
                <h1>Ask me anything</h1>
                <p>Your intelligent study companion — always ready to help you learn.</p>
            </div>

            <div class="chat-glass" id="chatBox">
                <div class="msg-welcome">
                    <div class="msg-avatar">✦</div>
                    <div class="msg-content">
                        <div class="msg-label">Study Buddy</div>
                        <div class="msg-text">Hey there! 👋 I'm your personal AI study companion.
Ask me anything — concepts, explanations, summaries, or quiz-style questions. Let's learn together! 🚀</div>
                    </div>
                </div>
            </div>

            <div class="hint-chips">
                <div class="chip" onclick="fillInput('Explain photosynthesis simply')">🌿 Photosynthesis</div>
                <div class="chip" onclick="fillInput('What is a prompt in AI?')">🤖 What is a prompt?</div>
                <div class="chip" onclick="fillInput('Summarize Newton\\'s laws of motion')">⚡ Newton\\'s Laws</div>
                <div class="chip" onclick="fillInput('How does the human heart work?')">❤️ Human Heart</div>
                <div class="chip" onclick="fillInput('Explain machine learning in simple terms')">🧠 Machine Learning</div>
            </div>

            <div class="input-wrapper">
                <input type="text" id="query" placeholder="Ask your question…" autocomplete="off" />
                <button class="send-btn" id="sendBtn" onclick="sendQuery()">
                    Ask
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="5" y1="12" x2="19" y2="12"/>
                        <polyline points="12 5 19 12 12 19"/>
                    </svg>
                </button>
            </div>

        </div>

        <script>
            const chatBox = document.getElementById("chatBox");
            const sendBtn = document.getElementById("sendBtn");
            const queryInput = document.getElementById("query");

            function fillInput(text) {
                queryInput.value = text;
                queryInput.focus();
            }

            function renderMarkdownLite(text) {
                return text
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\*(.*?)\*/g, '<em>$1</em>')
                    .replace(/^[*•-]\s+(.+)$/gm, '• $1');
            }

            async function sendQuery() {
                const query = queryInput.value.trim();
                if (!query) return;

                // Show user message
                chatBox.innerHTML = `
                    <div class="msg-welcome" style="margin-bottom:20px; opacity:0.65;">
                        <div class="msg-avatar" style="background: linear-gradient(135deg,#334155,#475569);">🧑</div>
                        <div class="msg-content">
                            <div class="msg-label" style="color:#64748b;">You</div>
                            <div class="msg-text">${renderMarkdownLite(query)}</div>
                        </div>
                    </div>
                    <div class="thinking">
                        <div class="msg-avatar">✦</div>
                        <div class="msg-content">
                            <div class="msg-label">Study Buddy</div>
                            <div class="thinking-dots">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    </div>`;

                sendBtn.disabled = true;
                queryInput.value = "";

                try {
                    const res = await fetch('/run', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: query })
                    });
                    const data = await res.json();

                    chatBox.innerHTML = `
                        <div class="msg-welcome" style="margin-bottom:20px; opacity:0.65;">
                            <div class="msg-avatar" style="background: linear-gradient(135deg,#334155,#475569);">🧑</div>
                            <div class="msg-content">
                                <div class="msg-label" style="color:#64748b;">You</div>
                                <div class="msg-text">${renderMarkdownLite(query)}</div>
                            </div>
                        </div>
                        <div class="msg-welcome">
                            <div class="msg-avatar">✦</div>
                            <div class="msg-content">
                                <div class="msg-label">Study Buddy</div>
                                <div class="msg-text">${renderMarkdownLite(data.response)}</div>
                            </div>
                        </div>`;

                } catch (err) {
                    chatBox.innerHTML = `
                        <div class="msg-welcome">
                            <div class="msg-avatar" style="background:linear-gradient(135deg,#be123c,#e11d48);">!</div>
                            <div class="msg-content">
                                <div class="msg-label" style="color:#fb7185;">Error</div>
                                <div class="msg-text">Something went wrong. Please try again.</div>
                            </div>
                        </div>`;
                }

                sendBtn.disabled = false;
                queryInput.focus();
            }

            queryInput.addEventListener("keypress", e => {
                if (e.key === "Enter") sendQuery();
            });
        </script>

    </body>
    </html>
    """

# 🤖 Agent Endpoint
@app.post("/run")
async def run_agent(request: Request):
    try:
        body = await request.json()
        user_input = body.get("message", "")

        session_id = str(uuid.uuid4())

        await session_service.create_session(
            app_name=APP_NAME,
            user_id="user",
            session_id=session_id
        )

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        response_text = ""

        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = event.content.parts[0].text

        return JSONResponse({"response": response_text})

    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}"})

# ❤️ Health Check
@app.get("/health")
def health():
    return {"status": "ok"}

# 🚀 Local run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)