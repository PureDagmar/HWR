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
1) Разметить бланк Form07 в Supervisely. Примерное время выполнения с использованием скрипта - 1 час.

- Разметить основную часть формы. Каждая ячейка должна быть отдельным классом. 
В основной части формы 23 строки по 32 ячейки - итого 736 классов. 
Наименование классов производить с "1" до "736".
- Разметить шапку формы. Каждая ячейка должна быть отдельным классом.
17 ячеек в первой строке, 31 - во второй, 11 - в третьей.
- Размечать с помощью rectangle. Rectangle должен включать в себя всю область внутри ячейки, допустимо включение dotted borders.

- Example 1:![Screenshot 2023-03-06 at 14 41 56](https://user-images.githubusercontent.com/84448247/223054896-b4b9488b-f02d-4d6c-97cc-6cf7ee90a462.png)

- Example 2:![Screenshot 2023-03-06 at 14 42 23](https://user-images.githubusercontent.com/84448247/223054905-3cc1b45d-0d95-4ee2-83b2-464d501911cf.png)

2) Нарезать недостающие данные из формы Form07. Примерное время выполнения 4 часа.
- Нарезать не менее 1000 элементов для класса Chekced и разместить в папку с именем **Х**.
-![Screenshot 2023-03-06 at 15 15 26](https://user-images.githubusercontent.com/84448247/223054963-a2fce0d9-727e-4ba1-9ec5-0128e81eded4.png)

- Нарезать не менее 1000 элементов для класса Empthy и разместить в папку с именем **E**.
- ![Screenshot 2023-03-06 at 15 15 43](https://user-images.githubusercontent.com/84448247/223054987-3579dfa6-3121-4806-9ce7-6b2314fad73a.png)

- Нарезать не менее 1000 элементов для дополнения класса O новыми элементами. 
- ![Screenshot 2023-03-06 at 15 15 16](https://user-images.githubusercontent.com/84448247/223055060-60d3f264-06c7-4317-8ce7-e22a134992d1.png)



