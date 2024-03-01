# Выполнение тестового задания на позицию Junior Python.

PDF с заданием вложен под именем `Задание Junior Flask.pdf`

---


### Запустить приложение:

**Шаг 1. Склонируй репозиторий:**
```
git clone git@github.com:tWoAlex/Junior-Python-test_task.git
```

**Шаг 2. Создай виртуальное окружение и установи зависимости:**

* Linux:
```
python3 -m venv env
```
```
source env/bin/activate
```

* Windows:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

**Шаг 3. Заполни файл `.env`:**
```
FLASK_DEBUG=False
MEDIA_DIR=media    # Название локальной папки, в которой будут хранится файлы пользователей API
```

**Шаг 4. Запусти приложение:**
```
flask run -h {адрес хоста} -p {номер порта}
```

---

Стек: **`Flask 3.0.2`**