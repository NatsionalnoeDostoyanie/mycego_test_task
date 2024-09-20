# The Test Task for Mycego for the vacancy of Full-Stack developer
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![python](https://img.shields.io/badge/Python-3.12.3-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
## Table of Contents
- [The Task](#the-task)
- [Setting up and running the project](#setting-up-and-running-the-project)
- [Usage](#usage)
- [Manage](#manage)
- [Logging](#logging)

## The Task
Also in the `media/` folder: [ТЗ Разработчик](<media/ТЗ Разработчик.pdf>)

**Тестовое задание на позицию “Full-stack разработчик”в компанию MYCEGO**

**Задание:**  
Создайте веб\-приложение на Flask или Django, которое взаимодействует с API Яндекс.Диска. Приложение должно реализовать следующий функционал:  
1\.	Просмотр файлов на Яндекс.Диске по вводу публичной ссылки (public\_key):  
После успешной авторизации пользователь должен видеть список всех файлов и папок, хранящихся по указанной публичной ссылке.  
2\.	Загрузка определенных файлов:  
Пользователь должен иметь возможность выбирать файлы из списка и загружать их на свой локальный компьютер через интерфейс веб\-приложения.  
Технические требования:  
•	Использовать Flask или Django в качестве фреймворка для веб\-приложения.  
•	Получать список файлов с Яндекс.Диска с помощью REST API.  
•	Реализовать возможность скачивания выбранных пользователем файлов с Яндекс.Диска на локальный компьютер.  
•	Приложение должно иметь простой веб\-интерфейс для отображения списка файлов и кнопок для их загрузки.  
Дополнительные требования:  
•	Для работы с API Яндекс.Диска можно использовать библиотеку requests/aiohttp или любую другую HTTP-клиентскую библиотеку.  
•	Документирование кода, аннотация типов.  
•	Код должен быть выложен на GitHub или аналогичный сервис, с историей коммитов.  
Критерии оценки:  
•	Корректность реализации авторизации и работы с API.  
•	Удобство и простота интерфейса.  
•	Читабельность и структурированность кода.  
•	Наличие инструкций по запуску и использованию приложения.  
•	Соответствие заданиям техническим и дополнительным требованиям.  
Опциональные задачи (необязательные, но будут плюсом):  
1\.	Реализовать систему фильтрации файлов по типу (например, только документы или только изображения).  
2\.	Возможность скачивания нескольких файлов одновременно.  
3\.	Реализовать кэширование списка файлов, чтобы не запрашивать его каждый раз с сервера.

**ВАЖНО\! Задание нужно отправить с ссылкой на документ в чат.**  
Обязательно при отправке тестового нужно указать сколько времени потратили на выполнение задания.  
**Желаем удачи\!**

## Setting up and running the project

**Clone** the project:
```sh
git clone https://github.com/NatsionalnoeDostoyanie/mycego_test_task.git
```

Go to the **project directory:**
```sh
cd mycego_test_task
```

Create **virtual environment:**
```sh
python -m venv venv
```
Activate **virtual environment:** \
**Linux:**
```sh
source venv/bin/activate
```
**Windows:**
```sh
venv\Scripts\activate
```

Install **requirements:**
```sh
pip install -r requirements.txt
```

**Run:**
```sh
cd scripts
```
```sh
python useful_scripts.py runserver
```

## Usage

Follow the **link:** \
`http://127.0.0.1:8000/api/v1/`

Then enter a **public url** to the Yandex Disk folder in the form of:
`https://disk.yandex.ru/d/...`

You will receive a **list of files and folders** located at the specified address. 
You can select files to **download** or **open an internal folder**.

When **downloading files**, they will be saved in the root directory in the `files/` folder 
(if it does not exist, it will be created automatically).

## Manage

While in the `mycego_test_task/scripts/` directory, you can:

**Run the Django server:**
```sh
python useful_scripts.py runserver
```
**Tidy up the code formatting:**
```sh
python useful_scripts.py linters
```
**Check for type errors:**
```sh
python useful_scripts.py mypy
```

## Logging

- There is a `logs/` folder in the repository root (if it does not exist, it is created automatically), 
where log files are created.
- The file created on the current day is called `logs`. Files created on voice days are named 
`logs.<file creation date>`. As of the current day (at 00:00), when starting to record a new log, 
file `logs` changes its name to `logs.<date of only that past day, which is also the file creation date>`, 
and a new empty file is created with the name `logs`, 
where this new log (and all subsequent logs of the next day) will be written.
- A total of 4 files can be in `logs/`: `logs` and three files created in the three-day window. 
All files older than three days are destroyed.
- The `logs` file writes all the logs of the current day of the `WARNING` levels and higher in the format 
`<level name> - <asctime> - <module> - <message>`.
- Logs of all levels in the same format are created in the console.
- Everything related to the configuration of the logging system is located in `settings/logging.py`.
