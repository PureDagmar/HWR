import numpy as np
import torch
from clearml import InputModel
from fastapi import APIRouter, Depends, UploadFile
from torchvision import transforms

from ..models import View
from ..token import has_access
from ..utils import file_to_img, process_result
from ..utils.align import write_cell_images
from ...settings import get_config

view_prefix = ''

router = APIRouter()
not_protect_router = APIRouter()

sc = get_config()
PROTECTED = [Depends(has_access)]

model = InputModel(name=sc.MODEL_NAME, only_published=True)
model = torch.jit.load(model.get_local_copy(), map_location=sc.device)
model = torch.jit.freeze(model)
model.to(sc.device)

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((sc.height, sc.width)),
])


@not_protect_router.get(path="/health", tags=["Health"])
async def health() -> str:
    return "I am alive"


@router.post(path="/inference", tags=["Inference"])
async def inference(blank: UploadFile):
    cell_images = write_cell_images(file_to_img(blank))
    answer_dict = {}
    for key in cell_images:
        labels_row = []
        for row in cell_images[key]:
            images = torch.stack(
                [transform(img) for img in row]
            ).to(sc.device)
            labels = model(images).detach().cpu().numpy()
            print(labels.shape)
            labels_row.append([process_result(label) for label in labels])
        answer_dict[key] = labels_row
    return answer_dict


view = View(
    router=router,
    not_protect_router=not_protect_router,
    prefix=view_prefix,
    PROTECTED=PROTECTED
)
