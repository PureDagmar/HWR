import datetime
from copy import deepcopy
from typing import Optional

import pytorch_lightning as pl
import torch
from clearml import OutputModel
from pytorch_lightning import Callback


class MySavingCallBack(Callback):
    def __init__(self):
        self.output_model = None
        self.score = None

    def setup(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule", stage: Optional[str] = None) -> None:
        self.score = 0
        self.output_model = OutputModel(name=f'OCRBlanksClassicationModel',
                                        label_enumeration=pl_module.class_to_idx,
                                        tags=[pl_module.hparams.model_name,
                                              datetime.datetime.utcnow().strftime('%Y_%m_%d')],
                                        )

    def on_validation_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        monitor_candidates = deepcopy(trainer.callback_metrics)
        if 'train_accuracy' not in monitor_candidates:
            return

        train_accuracy = monitor_candidates['train_accuracy'].float()
        train_loss = monitor_candidates['train_loss'].float()
        valid_accuracy = monitor_candidates['valid_accuracy'].float()
        valid_loss = monitor_candidates['valid_loss'].float()

        score = (train_accuracy + valid_accuracy) / (train_loss + valid_loss)

        if score > self.score:
            pl_module.to_torchscript(file_path=f'ocr_{pl_module.hparams.model_name}.pt', method='trace',
                                     example_inputs=torch.randn(
                                         pl_module.hparams.batch_size,
                                         3,
                                         pl_module.hparams.height,
                                         pl_module.hparams.width))
            self.output_model.update_weights(f'ocr_{pl_module.hparams.model_name}.pt')
            self.score = score
