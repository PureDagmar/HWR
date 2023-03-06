### Preparation
Install [poetry](https://python-poetry.org/docs/):
```commandline
curl -sSL https://install.python-poetry.org | python3 -
```
Install make:
```commandline
sudo apt install make
```
Setup environment:
```commandline
make setup
```
Activate environment:
```commandline
make activate
```

### Working with datasets
```python
from clearmltools.dataset import add_dataset, get_dataset

# Getting dataset:
dataset_id, dataset_path = get_dataset('Blanks')

# Adding dataset:
add_dataset("New_dataset", './datasets/New_dataset')
```
