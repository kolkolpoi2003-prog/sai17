#!/bin/bash
# ============================================
# Скрипт первоначального получения SSL сертификата
# Запускать ОДИН РАЗ на сервере после первого деплоя
# ============================================

set -e

# Загрузить переменные из .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

DOMAIN=${DOMAIN:-yarko-solntse.ru}
EMAIL=${EMAIL:-admin@yarko-solntse.ru}

echo "============================================"
echo "  Получение SSL сертификата для $DOMAIN"
echo "============================================"

# Шаг 1: Создать временный nginx конфиг (только HTTP)
echo ">>> Создаём временный nginx конфиг (только HTTP)..."
cat > nginx/default.conf.tmp <<'NGINX_CONF'
server {
    listen 80;
    server_name yarko-solntse.ru www.yarko-solntse.ru 37.252.19.159;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 'Site is being configured...';
        add_header Content-Type text/plain;
    }
}
NGINX_CONF

# Сохранить оригинальный конфиг
cp nginx/default.conf nginx/default.conf.bak
cp nginx/default.conf.tmp nginx/default.conf

# Шаг 2: Запустить nginx и web
echo ">>> Запускаем nginx..."
docker compose up -d nginx web

# Подождать запуск
echo ">>> Ждём 10 секунд для запуска..."
sleep 10

# Шаг 3: Получить сертификат
echo ">>> Запрашиваем сертификат у Let's Encrypt..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

# Шаг 4: Восстановить полный nginx конфиг
echo ">>> Восстанавливаем полный nginx конфиг с HTTPS..."
cp nginx/default.conf.bak nginx/default.conf
rm -f nginx/default.conf.tmp nginx/default.conf.bak

# Шаг 5: Перезапустить всё
echo ">>> Перезапускаем все сервисы..."
docker compose down
docker compose up -d

echo ""
echo "============================================"
echo "  SSL сертификат получен!"
echo "  Сайт доступен: https://$DOMAIN"
echo "============================================"
