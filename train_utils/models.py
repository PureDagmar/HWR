import torch
import torchvision
from torch import nn
from torchvision import transforms
from collections.abc import Sequence
from torchsummary import summary


class OCRBackbones(nn.Module):
    def __init__(self, model_name: str, input_sizes: Sequence[int], num_classes: int):
        super().__init__()
        self.num_classes = num_classes
        self.transforms = nn.Sequential(
            transforms.Resize(input_sizes),
            transforms.ConvertImageDtype(dtype=torch.float),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            # TODO: подобрать для нашего датасета
        )
        self.base_model = None
        self.__getattribute__(model_name)()

    def forward(self, x):
        out = self.transforms(x)
        out = self.base_model(out)
        out = torch.sigmoid(out)
        return out

    def mobilenet_small(self):
        self.base_model = torchvision.models.mobilenet_v3_small(
            weights=torchvision.models.MobileNet_V3_Small_Weights
        )
        self.base_model.classifier = nn.Sequential(
            nn.Linear(576, self.num_classes, True)
        )

    def resnet18(self):  # Скорее всего использовать не будем
        self.base_model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights)
        self.base_model.fc = nn.Sequential(
            nn.Linear(512, self.num_classes, bias=True)
        )

    def shufflenet_v2(self):
        self.base_model = torchvision.models.shufflenet_v2_x0_5(
            weights=torchvision.models.ShuffleNet_V2_X0_5_Weights
        )
        self.base_model.fc = nn.Sequential(
            nn.Linear(1024, self.num_classes, bias=True)
        )


if __name__ == '__main__':
    model = OCRBackbones(
        model_name='shufflenet_v2',
        input_sizes=(42, 30),
        num_classes=12
    )
    summary(model, input_size=(3, 42, 30), device="cpu")
