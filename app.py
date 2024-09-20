import logging
from fastapi import FastAPI
from src.query_builder import get_answer

logger = logging.getLogger("app.main")

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello"}


@app.post("/answer")
async def answer(question: str):
    logger.info("Question asked: %s", question)
    answer = get_answer(question=question)
    return {
        "answer": answer,
    }
