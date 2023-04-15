import cv2
import numpy as np


def hor_lines_cut(img, kernel_size=1):
    # Load image, convert to grayscale, Otsu's threshold
    result = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = np.ones((kernel_size, kernel_size), 'uint8')
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    # Detect horizontal lines
    min_len = int(img.shape[1] * 0.9)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_len, 1))
    detect_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    if len(cnts) >= 2:
        down_cnt = cnts[0]
        up_cnt = cnts[1]
        result = result[up_cnt[0][0][1]:down_cnt[0][0][1], :]
    elif len(cnts) == 1:
        up_cnt = cnts[0]
        result = result[up_cnt[0][0][1]:, :]
    if result.shape[0] < 90:
        if len(cnts) >= 2:
            result = hor_lines_cut(img[up_cnt[0][0][1]:, :])
        elif len(cnts) == 1:
            result = hor_lines_cut(img[:up_cnt[0][0][1], :], 4)
    return result