from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
import json
import uvicorn

app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str


@app.post("/chat")
def chat(req: ChatRequest):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=req.prompt
    )

    ai_text = response.output_text.strip()

    try:
        return json.loads(ai_text)
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw": ai_text
        }


if __name__ == "__main__":
    global client

    api_key = input("Enter your OpenAI API key: ").strip()
    client = OpenAI(api_key=api_key)

    print("\nStarting server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)