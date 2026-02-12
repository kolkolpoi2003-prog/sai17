# 🚀 Инструкция по публикации сайта yarko-solntse.ru

**Сервер:** VPS `37.252.19.159`  
**Домен:** `yarko-solntse.ru`  
**Стек:** Django + Gunicorn + Nginx + Docker + Let's Encrypt SSL

---

## 📋 Содержание

1. [Настройка DNS](#1-настройка-dns)
2. [Загрузка на GitHub](#2-загрузка-на-github)
3. [Подготовка VPS](#3-подготовка-vps)
4. [Клонирование и настройка](#4-клонирование-и-настройка)
5. [Первый запуск](#5-первый-запуск)
6. [Получение SSL](#6-получение-ssl-сертификата)
7. [Проверка](#7-проверка)
8. [Обновление сайта](#8-обновление-сайта)
9. [Полезные команды](#9-полезные-команды)

---

## 1. Настройка DNS

Зайдите в панель управления вашего доменного регистратора и создайте **A-записи**:

| Тип | Имя | Значение |
|-----|-----|----------|
| A | @ | 37.252.19.159 |
| A | www | 37.252.19.159 |

> ⏱ DNS обновляется от 5 минут до 48 часов. Можно проверить: `ping yarko-solntse.ru`

---

## 2. Загрузка на GitHub

### На вашем компьютере (Windows):

```bash
# Перейдите в папку проекта
cd C:\Users\mira\Desktop\sai1.7.4

# Инициализируйте Git (если ещё нет)
git init

# Добавьте все файлы
git add .

# Первый коммит
git commit -m "Initial commit: Django shop ready for deployment"

# Создайте репозиторий на GitHub (https://github.com/new)
# Название: например, yarko-solntse

# Подключите удалённый репозиторий (замените YOUR_USERNAME):
git remote add origin https://github.com/YOUR_USERNAME/yarko-solntse.git

# Отправьте код
git branch -M main
git push -u origin main
```

> ⚠️ **Важно:** Файл `.gitignore` уже настроен — секреты, база данных и виртуальное окружение НЕ попадут на GitHub.

---

## 3. Подготовка VPS

### Подключитесь к серверу:

```bash
ssh root@37.252.19.159
```

### Установите Docker и Docker Compose:

```bash
# Обновить систему
apt update && apt upgrade -y

# Установить зависимости
apt install -y ca-certificates curl gnupg lsb-release git

# Добавить GPG ключ Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Добавить репозиторий Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установить Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Проверить установку
docker --version
docker compose version
```

### Настройте файрвол:

```bash
# Открыть порты HTTP, HTTPS, SSH
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
ufw status
```

---

## 4. Клонирование и настройка

### На VPS:

```bash
# Клонируйте репозиторий
cd /opt
git clone https://github.com/YOUR_USERNAME/yarko-solntse.git
cd yarko-solntse

# Создайте файл .env из шаблона
cp .env.example .env

# Отредактируйте .env
nano .env
```

### В файле `.env` укажите:

```env
# Сгенерируйте ключ этой командой:
# python3 -c "import secrets; print(secrets.token_urlsafe(50))"
DJANGO_SECRET_KEY=ВАШ_УНИКАЛЬНЫЙ_СЕКРЕТНЫЙ_КЛЮЧ

DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yarko-solntse.ru,www.yarko-solntse.ru,37.252.19.159,localhost
CSRF_TRUSTED_ORIGINS=https://yarko-solntse.ru,https://www.yarko-solntse.ru
DOMAIN=yarko-solntse.ru
EMAIL=ваш-email@example.com
```

> Для генерации ключа прямо на сервере: `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`

---

## 5. Первый запуск

### Сначала запустите БЕЗ SSL для проверки:

Временно отредактируйте `nginx/default.conf`, чтобы оставить только HTTP-блок:

```bash
# Создайте временный nginx конфиг
cat > nginx/default.conf <<'EOF'
server {
    listen 80;
    server_name yarko-solntse.ru www.yarko-solntse.ru 37.252.19.159;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

```bash
# Соберите и запустите
docker compose up -d --build

# Проверьте что контейнеры работают
docker compose ps

# Посмотрите логи
docker compose logs -f
```

Откройте `http://37.252.19.159` в браузере — сайт должен работать!

---

## 6. Получение SSL сертификата

> ⚠️ **Перед этим шагом DNS должен быть настроен** — `yarko-solntse.ru` должен указывать на `37.252.19.159`.

```bash
# Запустите автоматический скрипт
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

Или вручную:

```bash
# 1. Получите сертификат
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email ваш-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d yarko-solntse.ru \
    -d www.yarko-solntse.ru

# 2. Восстановите полный nginx конфиг
git checkout nginx/default.conf

# 3. Перезапустите
docker compose down
docker compose up -d
```

Откройте `https://yarko-solntse.ru` — должен быть 🔒 замочек!

---

## 7. Проверка

```bash
# Все контейнеры запущены?
docker compose ps

# Логи Django
docker compose logs web

# Логи Nginx
docker compose logs nginx

# Проверка сайта
curl -I https://yarko-solntse.ru
```

### Создайте суперпользователя для админки:

```bash
docker compose exec web python manage.py createsuperuser
```

Затем зайдите: `https://yarko-solntse.ru/admin/`

---

## 8. Обновление сайта

Когда вы внесли изменения в код:

### На вашем компьютере (Windows):

```bash
cd C:\Users\mira\Desktop\sai1.7.4
git add .
git commit -m "описание изменений"
git push
```

### На VPS:

```bash
cd /opt/yarko-solntse
git pull
docker compose up -d --build
```

---

## 9. Полезные команды

| Команда | Описание |
|---------|----------|
| `docker compose up -d` | Запустить все сервисы |
| `docker compose down` | Остановить все сервисы |
| `docker compose logs -f` | Смотреть логи в реальном времени |
| `docker compose logs web` | Логи Django |
| `docker compose restart web` | Перезапустить Django |
| `docker compose exec web python manage.py createsuperuser` | Создать админа |
| `docker compose exec web python manage.py shell` | Django shell |
| `docker compose exec web python manage.py migrate` | Миграции |

### Автообновление SSL (cron):

```bash
# Добавьте в cron (раз в неделю)
crontab -e

# Вставьте строку:
0 3 * * 1 cd /opt/yarko-solntse && docker compose run --rm certbot renew && docker compose exec nginx nginx -s reload
```

---

## 🛡 Безопасность

Что уже настроено:
- ✅ Секретный ключ в `.env` (не в коде)
- ✅ `DEBUG=False` на сервере
- ✅ HTTPS через Let's Encrypt
- ✅ Security headers в Nginx
- ✅ CSRF protection
- ✅ Session cookie security
- ✅ HSTS headers
- ✅ `.gitignore` исключает секреты

### Рекомендации:
- Регулярно обновляйте: `docker compose pull && docker compose up -d`
- Делайте бэкапы SQLite: `docker compose exec web cp /app/data/db.sqlite3 /app/data/db_backup.sqlite3`
- Настройте SSH ключи вместо пароля
