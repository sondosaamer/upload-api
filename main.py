import os, uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from supabase import create_client

app = FastAPI()
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
MAX_SIZE = 10 * 1024 * 1024  # 10 MB

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(413, "File too large")
    path = f"{uuid.uuid4()}_{file.filename}"
    supabase.storage.from_("uploads").upload(
        path, data, {"content-type": file.content_type}
    )
    return {"path": path}