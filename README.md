# "Продуктовый помощник" (Foodgram)

## 1. Описание <a id=1></a>

Проект "Продуктовый помошник" (Foodgram) - сайт, на котором пользователи могут: 
  - регистрироваться
  - создавать свои рецепты и управлять ими (корректировать\удалять)
  - просматривать рецепты других пользователей
  - добавлять рецепты других пользователей в "Избранное" и в "Список покупок"
  - подписываться на других пользователей
  - скачать список ингредиентов для рецептов, добавленных в "Список покупок"


---
## 2. Команды для запуска <a id=2></a>

Перед запуском необходимо склонировать проект:
```bash
git clone git@github.com:Denmais/foodgram-project-react.git

```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Linux: source venv/bin/activate
```

И установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Далее необходимо собрать образы для фронтенда и бэкенда.
Из папки "./backend/" выполнить команду:
```bash
docker build -t username/foodgram_backend .
```

Из папки "./frontend/" выполнить команду:
```bash
docker build -t username/foodgram_frontend .
```

Из папки "./infra/" выполнить команду:

```bash
docker build -t username/foodgram_gateway .
```

После создания образов можно создавать и запускать контейнеры. 
Из папки "./infra/" выполнить команду:
```bash
docker-compose up -d
```

После успешного запуска контейнеров выполнить миграции:
```bash
docker-compose exec backend python manage.py migrate
```

Создать суперюзера (Администратора):
```bash
docker-compose exec backend python manage.py createsuperuser
```

Собрать статику:
```bash
docker-compose exec backend python manage.py collectstatic
```

Теперь доступность проекта можно проверить по адресу [http://127.0.0.1:8000]

---


## 3. Сайт <a id=3></a>
Адрес сайта:https://foodgramnew.zapto.org

admin: dens@dens.ru
admin_password: 123
