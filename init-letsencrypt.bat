@echo off
setlocal

set "domains=api.loralink.live"
set "rsa_key_size=4096"
set "data_path=./certbot"
set "email=your-email@example.com"
set "staging=0"

echo ### Creating directories...
if not exist "%data_path%\conf" mkdir "%data_path%\conf"
if not exist "%data_path%\www" mkdir "%data_path%\www"

echo ### Downloading recommended TLS parameters...
if not exist "%data_path%\conf\options-ssl-nginx.conf" (
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "%data_path%\conf\options-ssl-nginx.conf"
)
if not exist "%data_path%\conf\ssl-dhparams.pem" (
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "%data_path%\conf\ssl-dhparams.pem"
)

echo ### Creating dummy certificate for %domains%...
if not exist "%data_path%\conf\live\%domains%" mkdir "%data_path%\conf\live\%domains%"

docker compose run --rm --entrypoint "openssl req -x509 -nodes -newkey rsa:%rsa_key_size% -days 1 -keyout '/etc/letsencrypt/live/%domains%/privkey.pem' -out '/etc/letsencrypt/live/%domains%/fullchain.pem' -subj '/CN=localhost'" certbot

echo ### Starting nginx...
docker compose up --force-recreate -d nginx

echo ### Deleting dummy certificate for %domains%...
docker compose run --rm --entrypoint "rm -Rf /etc/letsencrypt/live/%domains% && rm -Rf /etc/letsencrypt/archive/%domains% && rm -Rf /etc/letsencrypt/renewal/%domains%.conf" certbot

echo ### Requesting Let's Encrypt certificate for %domains%...
if "%staging%"=="1" (
    set "staging_arg=--staging"
) else (
    set "staging_arg="
)

docker compose run --rm --entrypoint "certbot certonly --webroot -w /var/www/certbot %staging_arg% --email %email% -d %domains% --rsa-key-size %rsa_key_size% --agree-tos --force-renewal" certbot

echo ### Reloading nginx...
docker compose exec nginx nginx -s reload

echo Done! Your SSL certificate should now be active.
pause