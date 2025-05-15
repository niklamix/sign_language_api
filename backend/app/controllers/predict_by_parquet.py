import numpy as np
import pandas as pd
# python3 -m pip install ai-edge-litert
from ai_edge_litert.interpreter import Interpreter

from backend.app.config.path_settings import APP_TEMPLATES_PATH

ROWS_PER_FRAME = 543


def load_relevant_data_subset(data):
    n_frames = int(len(data) / ROWS_PER_FRAME)
    data = data.values.reshape(n_frames, ROWS_PER_FRAME, 3)
    return data.astype(np.float32)


def predict_sign_from_parquet(data):
    interpreter = Interpreter(model_path=f'{APP_TEMPLATES_PATH}/tflite/model.tflite')
    prediction_fn = interpreter.get_signature_runner("serving_default")

    train = pd.read_csv(f'{APP_TEMPLATES_PATH}/csv/train.csv')
    train['sign_ord'] = train['sign'].astype('category').cat.codes

    ORD2SIGN = train[['sign_ord', 'sign']].set_index('sign_ord').squeeze().to_dict()

    xyz_np = load_relevant_data_subset(data)
    prediction = prediction_fn(inputs=xyz_np)
    sign = prediction['outputs'].argmax()
    return ORD2SIGN[sign]
