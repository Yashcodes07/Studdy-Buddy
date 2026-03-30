import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

@app.post("/run")
async def run_agent(request: Request):
    body = await request.json()
    user_input = body.get("message", "")

    await session_service.create_session(
        app_name=APP_NAME,
        user_id="user",
        session_id="session_001"
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    )

    response_text = ""
    async for event in runner.run_async(
        user_id="user",
        session_id="session_001",
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text

    return JSONResponse({"response": response_text})

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
