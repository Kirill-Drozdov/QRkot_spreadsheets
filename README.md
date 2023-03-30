## QRkot

### О проекте
Данный проект представляет собой приложение для Благотворительного фонда поддержки котиков QRKot.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Технологии
```
aiogoogle
alembic
fastapi-users[sqlalchemy]
fastapi
uvicorn[standard]
sqlalchemy
```

### Как развернуть проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Kirill-Drozdov/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:

```
uvicorn app.main:app
```

## Об авторе проекта:
Проект выполнил студент Яндекс Практикума -
Дроздов К.С. (https://github.com/Kirill-Drozdov)
