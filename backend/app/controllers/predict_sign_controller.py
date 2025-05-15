import os
import tempfile

import pandas as pd

import backend.app.controllers.predict_by_parquet as pbp
import backend.app.controllers.video_to_parquet as vtp

from backend.app.config.path_settings import APP_TEMPLATES_PATH


async def predict_sign_by_video(video):
    file_ext = video.filename.split(".")[-1]
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}')
    try:
        content = await video.read()
        temp_video.write(content)
        temp_video.close()

        landmarks = vtp.do_capture_loop(temp_video.name)
        landmarks = pd.concat(landmarks).reset_index(drop=True)
        data = landmarks[['x', 'y', 'z']]
        return pbp.predict_sign_from_parquet(data)
    finally:
        # Удаляем файл в случае ошибки
        os.unlink(temp_video.name)


async def all_words():
    df = pd.read_csv(f'{APP_TEMPLATES_PATH}/csv/train.csv')
    return df['sign'].unique().tolist()
