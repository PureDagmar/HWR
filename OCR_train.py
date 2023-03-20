import argparse
import datetime
from glob import glob

import pytorch_lightning as pl
from clearml import Task
from pytorch_lightning.loggers import TensorBoardLogger

from clearmltools.dataset import get_dataset
from train_utils.callbacks import MySavingCallBack
from train_utils.pl_models import Classifier

MINIO_HOST = "78.140.23.134:9000"


def eval_num_classes(dataset_name: str) -> int:
    _, dt_path = get_dataset(dataset_name)
    all_folders = glob(f'{dt_path}/*')
    return len(all_folders)


if __name__ == '__main__':
    print(f"Dataset labels: {eval_num_classes('Symbols')}")
    pl.seed_everything(0)

    parser = argparse.ArgumentParser(description="BlankOCR Train process")
    parser.add_argument("--device", default="cpu", type=str)
    parser.add_argument("--model_name", default="mobilenet_small", type=str)
    parser.add_argument("--learning_rate", default=3e-4, type=float)
    parser.add_argument("--train_size", default=0.75, type=float)
    parser.add_argument("--batch_size", default=256, type=int)
    parser.add_argument("--width", default=30, type=int)
    parser.add_argument("--height", default=42, type=int)
    parser.add_argument("--max_epochs", default=256, type=int)
    args = parser.parse_args()

    task = Task.init(
        project_name="BlanksOCR",
        task_name=f"OCR_{args.model_name}_{datetime.datetime.now().strftime('%Y-%m-%d-%H')}",
        output_uri=f"s3://{MINIO_HOST}/datasets",
        reuse_last_task_id=True,
        auto_connect_frameworks={'tensorboard': True, 'pytorch': False}
    )

    saving_callback = MySavingCallBack()
    lr_monitor = pl.callbacks.LearningRateMonitor(logging_interval='epoch')
    tb_logger = TensorBoardLogger(save_dir="logs/")

    trainer = pl.Trainer(
        accelerator=args.device,
        callbacks=[saving_callback, lr_monitor],
        logger=tb_logger,
        max_epochs=args.max_epochs
    )

    classifier = Classifier(
        model_name=args.model_name,
        input_sizes=(args.height, args.width),
        num_classes=eval_num_classes('Symbols'),
        learning_rate=args.learning_rate,
        train_size=args.train_size,
        batch_size=args.batch_size,
    )
    trainer.fit(classifier)
