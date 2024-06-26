import os
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)

import requests
url = "https://asr.hpda.vn/stt"
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel

from constants import ERROR_MESSAGES
from utils.utils import (
    decode_token,
    get_current_user,
    get_verified_user,
    get_admin_user,
)
from utils.misc import calculate_sha256

from config import CACHE_DIR, UPLOAD_DIR, WHISPER_MODEL, WHISPER_MODEL_DIR
from pydantic import BaseModel, ConfigDict
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ASR(BaseModel):
    file: UploadFile = File(...),
    lang: str



@app.post("/transcribe")
@app.post("/transcribe/{lang}")
def transcribe(
    lang: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    print(lang)
    print(file.content_type)
    print(file)
    if file.content_type not in ["audio/mpeg", "audio/wav"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.FILE_NOT_SUPPORTED,
        )

    try:
        filename = file.filename
        file_path = f"{UPLOAD_DIR}/{filename}"
        contents = file.file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            f.close()

        
        files = {'file': open(file_path, 'rb')}
        if lang == "en" :
            response = requests.post(url, files=files, data = {'language': "English"})
        else :
            response = requests.post(url, files=files, data={'language' : "Vietnamese"})

        os.remove(file_path)
        #transcript = "".join([segment.text for segment in list(segments)])

        return response.json()

    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT(e),
        )
