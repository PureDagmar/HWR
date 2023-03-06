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

## Homeworks
### First HW (27/02)
GO to the file **MLPipline.svg** to see project pipline.

### Second HW (6/03)
#### Составить ТЗ для разметчиков
1) Разметить бланк Form07. Примерное время выполнения с использованием скрипта - 1 час.
![Form07](https://user-images.githubusercontent.com/84448247/223049321-0608e3e3-17ff-42df-8003-5bbdd5a0d67a.png)
- Разметить основную часть формы. Каждая ячейка должна быть отдельным классом. 
В основной части формы 23 строки по 32 ячейки - итого 736 классов. 
Наименование классов производить с "1" до "736".
- Разметить шапку формы. Каждая ячейка должна быть отдельным классом.
17 ячеек в первой строке, 31 - во второй, 11 - в третьей.
- Размечать с помощью rectangle. Rectangle должен включать в себя всю область внутри ячейки, допустимо включение dotted borders. См. пример ниже.
![Screenshot 2023-03-06 at 14 42 23](https://user-images.githubusercontent.com/84448247/223048123-fff19c9b-36e5-41ac-a83c-e4856a8f9dfe.png)
![Screenshot 2023-03-06 at 14 41 56](https://user-images.githubusercontent.com/84448247/223048138-4ad64663-4af1-4d7a-8a7d-dff86ba4f7ee.png)
2) Нарезать недостающие данные из формы Form07. Примерное время выполнения 4 часа.
- Нарезать не менее 1000 элементов для класса Chekced и разместить в папку с именем **Х**.
![Screenshot 2023-03-06 at 15 01 17](https://user-images.githubusercontent.com/84448247/223051854-1f06d741-3536-47af-a040-898c8b48e5fa.png)
- Нарезать не менее 1000 элементов для класса Empthy и разместить в папку с именем **E**.
![Screenshot 2023-03-06 at 15 02 07](https://user-images.githubusercontent.com/84448247/223051891-6b07c961-4823-4592-a8b1-1ba94e437cbe.png)
- Нарезать не менее 1000 элементов для дополнения класса O новыми элементами. 
![Screenshot 2023-03-06 at 15 01 54](https://user-images.githubusercontent.com/84448247/223051982-4a98e432-75a9-42df-a631-14025f75b104.png)


