from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid

from app.services.document_loader import extract_text_from_pdf

app = FastAPI(title="RAG Assistant API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    file_path = UPLOAD_DIR / f"{uuid.uuid4()}.pdf"

    content = await file.read()
    file_path.write_bytes(content)

    pages = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "total_pages": len(pages),
        "extracted_pages": pages
    }
