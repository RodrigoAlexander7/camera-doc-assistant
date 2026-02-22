from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.gemini_service import gemini_service

router = APIRouter()


@router.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Uploads an image, analyzes it using Gemini, and returns the classification and explanation.
    If the document is a legal document, it also returns the response from the external legal copilot.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        content = await file.read()
        result = await gemini_service.analyze_image(content, file.content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
