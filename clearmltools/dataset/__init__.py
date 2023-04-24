import os.path
import typing as tp
from pathlib import Path

from clearml.datasets import Dataset

MINIO_HOST = "78.140.23.134:9000"
PROJECT = "BlanksOCR"


def add_dataset(
        name: str,
        path_to_dataset_folder: str | Path,
        minio_host: str = MINIO_HOST,
        project: str = PROJECT,
        tags: tp.Sequence[str] | None = None
):
    assert os.path.exists(path_to_dataset_folder), \
        FileNotFoundError(f"There is no folder with name {path_to_dataset_folder}")

    new_dataset = Dataset.create(dataset_project=project,
                                 output_uri=f"s3://{minio_host}/datasets",
                                 dataset_tags=tags,
                                 dataset_name=name)

    new_dataset.add_files(path_to_dataset_folder)
    new_dataset.upload()
    new_dataset.finalize()


def get_dataset(
        name: str,
        project: str = PROJECT,
        version: str | None = None
) -> (str, str):
    dataset = Dataset.get(
        dataset_project=project,
        dataset_name=name,
        only_completed=True,
        dataset_version=version
    )
    parent_id = dataset.id
    dataset_path = dataset.get_local_copy()
    return parent_id, dataset_path


if __name__ == "__main__":
    add_dataset('Blanks', '/home/gmyrseve7n/edu/HWR_Numbers/datasets/Forms-20230224T080614Z-001/Forms')
