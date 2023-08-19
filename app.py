from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from typing import Annotated
import secrets

app = FastAPI()

@app.get("/")
async def _hello():
    return { "msg": "Hello World" }

@app.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
    token: Annotated[str, Form()]
):
    try:
        if file.content_type:
            extension = file.content_type.split("/")
            content = await file.read()
            disk_filename = f"{secrets.token_urlsafe(10)}.{extension[-1]}"

            # write the file to disk
            with open(disk_filename, "wb") as image_file:
                image_file.write(content)
            return { "msg": f"wrote file to {disk_filename}" }
    except:
        return { "msg": "Failed" }

