import yaml

import cv2
import numpy as np

with open('config/utils_config.yml') as stream:
    config = yaml.safe_load(stream)['shapeCorrection']


def align_images(img):
    imReference = cv2.imread(config['mask'], cv2.IMREAD_COLOR)
    # Change size
    if not imReference.shape[1] * 0.90 < img.shape[1] < imReference.shape[1] * 1.1:
        img = cv2.resize(img, (imReference.shape[1], imReference.shape[0]))
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(imReference, cv2.COLOR_BGR2GRAY)
    # Detect ORB features and compute descriptors
    orb = cv2.ORB_create(WTA_K=3)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
    # Match features
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)  # , crossCheck=True)
    matches = matcher.match(descriptors1, descriptors2, None)
    matches = sorted(matches, key=lambda x: x.distance)
    # Remove not so good matches
    numGoodMatches = int(len(matches) * config['goodMatchPercent'])
    matches = matches[:numGoodMatches]
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    # Find homography
    h, mask = cv2.estimateAffinePartial2D(points1, points2, ransacReprojThreshold=9)
    # Use homography
    height, width, channels = imReference.shape
    im1Reg = cv2.warpAffine(img, h, (width, height))
    return im1Reg