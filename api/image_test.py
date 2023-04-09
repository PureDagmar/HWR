import cv2
import torch
from clearml import InputModel
from torchvision import transforms

from service.api.utils.align import write_cell_images
from service.settings import get_config

sc = get_config()
model = InputModel(name=sc.MODEL_NAME, only_published=True)
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
        for img in row:
            tens = transform(img)
            # img = tens.permute(1, 2, 0).numpy()
            tens = tens[None, :]
            answer = model(tens.to(sc.device)).detach().cpu().numpy()
            print(answer)
            cv2.imshow('test', img)
            cv2.waitKey()

