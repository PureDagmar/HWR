import time
from multiprocessing import cpu_count
from typing import Any, Sequence

import cv2
import pytorch_lightning as pl
import torch.optim
import torchmetrics
from torchvision import transforms
from torch.nn import functional as F
from torch.utils.data import random_split, DataLoader
from torchvision.datasets import ImageFolder

from clearmltools.dataset import get_dataset
from models import OCRBackbones


class Classifier(pl.LightningModule):
    def __init__(
            self,
            model_name: str,
            input_sizes: Sequence[int],
            num_classes: int,
            learning_rate: float = 3e-4,
            train_size: float = 0.66,
            batch_size: int = 256
    ):
        super().__init__()
        self.class_to_idx = None
        self.valid_part: ImageFolder | None = None
        self.train_part: ImageFolder | None = None
        self.learning_rate = learning_rate
        self.save_hyperparameters()
        self.hparams.width = input_sizes[1]
        self.hparams.height = input_sizes[0]
        self.backbone = OCRBackbones(
            model_name=model_name,
            input_sizes=input_sizes,
            num_classes=num_classes
        )
        self.accuracy = torchmetrics.Accuracy(task='multiclass', num_classes=num_classes)

    def forward(self, x) -> Any:
        return self.backbone(x)

    def configure_optimizers(self) -> Any:
        optimizer = torch.optim.RAdam(self.parameters(), lr=self.learning_rate)
        scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.90)
        return [optimizer], [scheduler]

    def prepare_data(self) -> None:
        _, dataset_path = get_dataset("Symbols")
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((self.hparams.height, self.hparams.width)),

        ])
        dataset = ImageFolder(dataset_path, transform=transform)
        self.class_to_idx = dataset.class_to_idx
        len_dataset = len(dataset)
        train_size = int(len_dataset * self.hparams.train_size)
        valid_size = len_dataset - train_size
        self.train_part, self.valid_part = random_split(
            dataset,
            lengths=[train_size, valid_size],
            generator=torch.Generator()
        )

    def train_dataloader(self):
        return DataLoader(self.train_part, shuffle=True, num_workers=4, batch_size=self.hparams.batch_size)

    def val_dataloader(self):
        return DataLoader(self.valid_part, shuffle=False, num_workers=2, batch_size=self.hparams.batch_size)

    def training_step(self, batch, *args: Any, **kwargs: Any):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        accuracy = self.accuracy(y_hat, y)
        self.log('train_accuracy', accuracy)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, *args: Any, **kwargs: Any):
        x, y = batch

        start = time.time()
        y_hat = self(x)
        speed = time.time() - start

        speed = speed / self.hparams.batch_size

        loss = F.cross_entropy(y_hat, y)
        accuracy = self.accuracy(y_hat, y)
        self.log('valid_accuracy', accuracy)
        self.log('valid_loss', loss)
        self.log('speed', speed)
