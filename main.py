from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from ocr_engine import extract_text_from_image
from utils import create_docx
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

@app.post("/ocr/upload-multiple/")
async def ocr_multiple_images(files: List[UploadFile] = File(...)):
    # 1. Validation: Limit to 20 files
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 files allowed.")

    extracted_texts = []

    # 2. Process each file
    for file in files:
        if not file.content_type.startswith("image/"):
            continue # Or raise an error
            
        content = await file.read()
        text = extract_text_from_image(content)
        extracted_texts.append(text)

    # 3. Create the Word Document
    docx_stream = create_docx(extracted_texts)

    # 4. Return as a downloadable file
    return StreamingResponse(
        docx_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=extracted_ocr_data.docx"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)