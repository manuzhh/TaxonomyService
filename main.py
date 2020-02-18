from fastapi import FastAPI
from typing import List
from Categorizer import Categorizer


app = FastAPI()


@app.get("/categorization")
async def get_labels(texts: List[str]):
    return Categorizer.categorize_texts(texts)
