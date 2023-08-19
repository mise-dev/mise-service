from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import Annotated
import secrets

app = FastAPI()

@app.get("/")
async def _hello():
    return { "msg": "Hello World" }
