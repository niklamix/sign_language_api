import random

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

import backend.app.controllers.predict_sign_controller as predict_controller

router = APIRouter(prefix="/predict", tags=["predictions"])


@router.post("/by_video")
async def predict_sign_by_video(
        video: UploadFile = File(...)
):
    file_ext = video.filename.split(".")[-1]
    if file_ext not in ["mp4", "avi", "mov", "gif", "webm"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        processing_result = await predict_controller.predict_sign_by_video(video)

        return JSONResponse({
            "status": "success",
            "result": processing_result
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in processing video: {str(e)}")


@router.get("/all_words")
async def get_all_word_for_prediction():
    try:
        result = await predict_controller.all_words()

        return JSONResponse({
            "status": "success",
            "count": len(result),
            "result": result
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in get words: {str(e)}")

@router.get("/random_word")
async def get_random_word_for_prediction():
    try:
        all_words = await predict_controller.all_words()
        return JSONResponse({
            "status": "success",
            "word": random.choice(all_words)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in get word: {str(e)}")