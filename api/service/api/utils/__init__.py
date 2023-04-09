import io

import cv2
import numpy as np
from fastapi import UploadFile


def file_to_img(file: UploadFile) -> np.ndarray:
    file = file.file.read()
    file_bytes = np.asarray(
        bytearray(io.BytesIO(file).read()),
        dtype=np.uint8
    )
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


def process_result(arr: np.ndarray) -> str:
    print(arr)
    label = np.argmax(arr)
    if label == 10:
        return ""
    if label == 11:
        return "X"
    return str(label)
