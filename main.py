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

# 🌐 Modern UI
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Study Buddy AI</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0f172a;
                color: #e5e7eb;
            }

            .header {
                display: flex;
                align-items: center;
                padding: 15px 25px;
                background: #020617;
                border-bottom: 1px solid #1e293b;
            }

            .logo {
                font-size: 20px;
                font-weight: bold;
                color: #38bdf8;
            }

            .container {
                max-width: 800px;
                margin: 40px auto;
                padding: 20px;
            }

            .chat-box {
                background: #020617;
                padding: 20px;
                border-radius: 10px;
                min-height: 300px;
                border: 1px solid #1e293b;
                margin-bottom: 20px;
                white-space: pre-wrap;
            }

            .input-box {
                display: flex;
                gap: 10px;
            }

            input {
                flex: 1;
                padding: 12px;
                border-radius: 8px;
                border: none;
                outline: none;
                background: #1e293b;
                color: white;
            }

            button {
                padding: 12px 18px;
                background: #38bdf8;
                border: none;
                border-radius: 8px;
                color: black;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #0ea5e9;
            }
        </style>
    </head>

    <body>

        <div class="header">
            <div class="logo">📘 Study Buddy</div>
        </div>

        <div class="container">
            <div id="response" class="chat-box">
Welcome! Ask me anything 📚
            </div>

            <div class="input-box">
                <input type="text" id="query" placeholder="Ask your question..." />
                <button onclick="sendQuery()">Ask</button>
            </div>
        </div>

        <script>
            async function sendQuery() {
                const inputBox = document.getElementById("query");
                const query = inputBox.value;

                if (!query) return;

                document.getElementById("response").innerText = "⏳ Thinking...";
                inputBox.value = "";

                try {
                    const res = await fetch('/run', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: query })
                    });

                    const data = await res.json();
                    document.getElementById("response").innerText = data.response;
                } catch (error) {
                    document.getElementById("response").innerText = "❌ Error occurred";
                }
            }

            // Press Enter to send
            document.getElementById("query").addEventListener("keypress", function(e) {
                if (e.key === "Enter") {
                    sendQuery();
                }
            });
        </script>

    </body>
    </html>
    """

# 🤖 Agent Endpoint (FIXED)
@app.post("/run")
async def run_agent(request: Request):
    try:
        body = await request.json()
        user_input = body.get("message", "")

        # ✅ NEW SESSION EVERY REQUEST (IMPORTANT FIX)
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


# 🚀 Local run (optional)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)