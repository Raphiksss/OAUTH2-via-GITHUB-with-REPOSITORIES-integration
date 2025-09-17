# auth\_via\_github

Приложение на **FastAPI** с авторизацией через **GitHub OAuth**.

---

## Описание

Это минимальное приложение на FastAPI, которое позволяет пользователям входить через GitHub.
После авторизации приложение получает данные пользователя с GitHub и возвращает их в виде JSON.

---

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/kirillysz/auth_via_github.git
cd auth_via_github
```

2. Создайте файл `.env` в корне проекта со следующими переменными:

```env
GITHUB_CLIENT_ID=YOUR_CLIENT_ID
GITHUB_CLIENT_SECRET=YOUR_CLIENT_SECRET
GITHUB_REDIRECT_URI=http://localhost:8000/auth/github/callback
SECRET_KEY=YOUR_SECRET_KEY
```

> **Важно:** `GITHUB_REDIRECT_URI` должен совпадать с `Authorization callback URL` в настройках вашего GitHub OAuth приложения.

3. Поднимите Docker контейнер:

```bash
docker compose up --build -d
```

4. Откройте браузер и перейдите по адресу:

```
http://localhost:8000/auth/github
```

Вы будете перенаправлены на GitHub для авторизации, а после успешного логина данные пользователя вернутся в виде JSON на `/auth/github/callback`.

---

## Структура проекта

```
auth_via_github/
├─ app/
│  ├─ main.py
│  ├─ routes/
│  └─ config.py
├─ .env
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

---

## Требования

* Python 3.13+
* FastAPI
* Authlib
* Starlette
* itsdangerous
* Docker

---
