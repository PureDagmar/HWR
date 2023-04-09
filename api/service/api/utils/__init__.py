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


def process_result(arr: np.ndarray, labels: dict) -> str:
    label = np.argmax(arr)
    label = labels[int(label)]
    return label


def process_image(img: np.ndarray) -> np.ndarray | None:
    print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img[gray_img < 240] = 0
    img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
    return img
