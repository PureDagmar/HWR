import random
from glob import glob

import cv2
import torch
from clearml import InputModel, Dataset
from torchvision import transforms

from service.api.utils import process_result
from service.api.utils.align import write_cell_images
from service.settings import get_config

sc = get_config()
model = InputModel(name=sc.MODEL_NAME, only_published=True)
labels = {v: k for k, v in model.labels.items()}
print(labels)
model = torch.jit.load(model.get_local_copy(), map_location=sc.device)
model = torch.jit.freeze(model)
model.to(sc.device)
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((sc.height, sc.width)),
])

image = cv2.imread("./service/api/data/13328-processed-2.png")
cell_images = write_cell_images(image)
for key in cell_images:
    labels_row = []
    for row in cell_images[key]:
        random.shuffle(row)
        for img in row:

            tens = transform(img)
            tens = tens[None, :]
            answer = model(tens.to(sc.device)).detach().cpu().numpy()
            print(process_result(answer, labels))
            cv2.imshow('test', img)
            cv2.waitKey()

# dataset = Dataset.get(
#         dataset_project="BlanksOCR",
#         dataset_name="SymbolsText",
#         only_completed=True
#     )
# parent_id = dataset.id
# dataset_path = dataset.get_local_copy()
# all_imgs = glob(dataset_path + '/*/*')
# random.shuffle(all_imgs)
# print(len(all_imgs))
# for img in all_imgs:
#     img = cv2.imread(img)
#     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # print(gray_img)
#     # gray_img[gray_img < 240] = 0
#     # print(gray_img)
#     # img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)
#     tens = transform(img)
#     # img = tens.permute(1, 2, 0).numpy()
#     tens = tens[None, :]
#     answer = model(tens.to(sc.device)).detach().cpu().numpy()
#     print(process_result(answer, labels))
#     cv2.imshow('test', img)
#     cv2.waitKey()
