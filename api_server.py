from fastapi import FastAPI
from pydantic import BaseModel
from main_controller import generate_solution
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

api_key = os.getenv("GROQ_API_KEY")


class RequestModel(BaseModel):
    prompt: str


@app.post("/generate")
def generate(data: RequestModel):

    result, intent, steps, diagram = generate_solution(data.prompt, api_key)

    return {
        "hardware": intent,
        "steps": steps,
        "diagram": diagram,
        "result": result
    }