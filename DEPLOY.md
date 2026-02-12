# 🚀 Инструкция по публикации сайта yarko-solntse.ru

**Сервер:** VPS `37.252.19.159`  
**Домен:** `yarko-solntse.ru`  
**GitHub:** `https://github.com/kolkolpoi2003-prog/sai17.git`

---

## ШАГ 1. Настройка DNS (делается НЕ на сервере)

Зайдите в панель вашего доменного регистратора и создайте A-записи:

| Тип | Имя | Значение |
|-----|-----|----------|
| A | @ | 37.252.19.159 |
| A | www | 37.252.19.159 |

> ⏱ DNS обновляется от 5 минут до 48 часов. Проверить: `ping yarko-solntse.ru`

---

## ШАГ 2. Подключиться к серверу

Откройте терминал на вашем компьютере и введите:

```bash
ssh root@37.252.19.159
```

Введите пароль от VPS. **Все остальные команды выполняются на сервере.**

---

## ШАГ 3. Установить Docker на сервер

Выполняйте команды по одной:

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

# Проверить что Docker установился
docker --version
docker compose version
```

---

## ШАГ 4. Открыть порты в файрволе

```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
```

Когда спросит — нажмите `y` и Enter.

---

## ШАГ 5. ⬇️ ЗАГРУЗИТЬ ПРОЕКТ С GITHUB НА СЕРВЕР

**Вот здесь мы скачиваем ваш проект с GitHub на сервер:**

```bash
cd /opt
git clone https://github.com/kolkolpoi2003-prog/sai17.git
cd sai17
```

После этой команды все файлы проекта окажутся на сервере в папке `/opt/sai17/`.

Проверить что файлы на месте:
```bash
ls -la
```

Вы должны увидеть: `Dockerfile`, `docker-compose.yml`, `manage.py`, `nginx/` и т.д.

---

## ШАГ 6. Создать файл .env с настройками

```bash
# Скопировать шаблон
cp .env.example .env

# Сгенерировать секретный ключ
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

Скопируйте сгенерированный ключ, затем откройте .env для редактирования:

```bash
nano .env
```

Замените значения:

```env
DJANGO_SECRET_KEY=ВСТАВЬТЕ_СГЕНЕРИРОВАННЫЙ_КЛЮЧ_СЮДА
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yarko-solntse.ru,www.yarko-solntse.ru,37.252.19.159,localhost
CSRF_TRUSTED_ORIGINS=https://yarko-solntse.ru,https://www.yarko-solntse.ru
DOMAIN=yarko-solntse.ru
EMAIL=ваш-email@example.com
```

Сохраните: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## ШАГ 7. Первый запуск (без SSL, для проверки)

Сначала запустим с простым HTTP чтобы убедиться что всё работает:

```bash
# Создаём временный nginx конфиг (без SSL)
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
# Собрать и запустить
docker compose up -d --build
```

Подождите 1-2 минуты, затем проверьте:

```bash
# Все контейнеры работают?
docker compose ps

# Посмотреть логи (Ctrl+C чтобы выйти)
docker compose logs -f
```

Откройте в браузере: `http://37.252.19.159` — должен появиться сайт!

---

## ШАГ 8. Получить SSL сертификат (https://)

> ⚠️ DNS уже должен работать — `yarko-solntse.ru` должен указывать на `37.252.19.159`.
> Проверить: `ping yarko-solntse.ru` (на вашем компьютере)

```bash
# Получить сертификат
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email ваш-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d yarko-solntse.ru \
    -d www.yarko-solntse.ru
```

Если успешно — восстанавливаем полный nginx конфиг с HTTPS:

```bash
# Загрузить оригинальный nginx конфиг из GitHub
git checkout nginx/default.conf

# Перезапустить всё
docker compose down
docker compose up -d
```

Откройте `https://yarko-solntse.ru` — должен быть 🔒 замочек!

---

## ШАГ 9. Создать админа

```bash
docker compose exec web python manage.py createsuperuser
```

Введите логин, email, пароль. Затем зайдите: `https://yarko-solntse.ru/admin/`

---

## ШАГ 10. Автообновление SSL (cron)

```bash
crontab -e
```

Добавьте строку в конец файла:

```
0 3 * * 1 cd /opt/sai17 && docker compose run --rm certbot renew && docker compose exec nginx nginx -s reload
```

---

## 🔄 Как обновлять сайт в дальнейшем

### 1. На вашем компьютере (Windows) — загрузить изменения на GitHub:

```bash
cd C:\Users\mira\Desktop\sai1.7.4
git add .
git commit -m "описание что изменили"
git push
```

### 2. На сервере — скачать изменения с GitHub и перезапустить:

```bash
ssh root@37.252.19.159
cd /opt/sai17
git pull
docker compose up -d --build
```

Всё! Сайт обновится за 1-2 минуты.

---

## 📋 Полезные команды (на сервере)

| Команда | Описание |
|---------|----------|
| `docker compose ps` | Статус контейнеров |
| `docker compose logs -f` | Логи в реальном времени |
| `docker compose logs web` | Логи Django |
| `docker compose restart web` | Перезапустить Django |
| `docker compose down` | Остановить всё |
| `docker compose up -d` | Запустить всё |
| `docker compose exec web python manage.py createsuperuser` | Создать админа |
| `docker compose exec web python manage.py shell` | Django shell |
