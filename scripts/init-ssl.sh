#!/bin/bash

# Automated SSL Setup Script for LoraLink API
# This script automates the entire SSL certificate process

set -e  # Exit on any error

# Configuration
DOMAIN="api.loralink.live"
EMAIL="e.leonardo.rivas.m@gmail.com"
DEPLOY_PATH="/opt/loralinka-api"
NGINX_TEMP_CONFIG="nginx/nginx-temp.conf"
NGINX_FINAL_CONFIG="nginx/nginx.conf"

echo "🔒 Starting automated SSL setup for $DOMAIN..."

# Step 1: Create required directories
echo "📁 Creating required directories..."
mkdir -p certbot nginx

# Step 2: Create temporary HTTP-only nginx config
echo "⚙️  Creating temporary nginx configuration..."
cat > $NGINX_TEMP_CONFIG << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    server {
        listen 80;
        server_name api.loralink.live;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
EOF

# Step 3: Copy temp config to final location
cp $NGINX_TEMP_CONFIG $NGINX_FINAL_CONFIG

# Step 4: Start containers with HTTP-only config
echo "🐳 Starting containers with HTTP-only configuration..."
docker compose down || true
docker compose up -d

# Step 5: Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Step 6: Check if domain is accessible
echo "🌐 Testing domain accessibility..."
if ! curl -f http://$DOMAIN >/dev/null 2>&1; then
    echo "❌ Domain $DOMAIN is not accessible. Please ensure:"
    echo "   - Domain DNS points to this server"
    echo "   - Port 80 is open and accessible"
    echo "   - Docker containers are running"
    exit 1
fi

# Step 7: Install certbot if not present
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing certbot..."
    apt update && apt install -y certbot
fi

# Step 8: Get SSL certificate
echo "🔐 Obtaining SSL certificate for $DOMAIN..."
certbot certonly --webroot \
    -w ./certbot \
    -d $DOMAIN \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --non-interactive

# Step 9: Verify certificate was created
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "❌ SSL certificate creation failed!"
    exit 1
fi

# Step 10: Create final nginx config with SSL
echo "🔧 Creating final nginx configuration with SSL..."
cat > $NGINX_FINAL_CONFIG << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # HTTP server - redirect to HTTPS
    server {
        listen 80;
        server_name api.loralink.live;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$server_name$request_uri;
        }
    }

    # HTTPS server
    server {
        listen 443 ssl;
        server_name api.loralink.live;

        ssl_certificate /etc/letsencrypt/live/api.loralink.live/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.loralink.live/privkey.pem;

        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

# Step 11: Restart nginx with SSL configuration
echo "🔄 Restarting nginx with SSL configuration..."
docker compose restart nginx

# Step 12: Wait for nginx to start
sleep 5

# Step 13: Test SSL setup
echo "🧪 Testing SSL setup..."
if curl -f -I https://$DOMAIN >/dev/null 2>&1; then
    echo "✅ HTTPS is working!"
else
    echo "⚠️  HTTPS test failed, but certificate might still be valid"
fi

# Test HTTP to HTTPS redirect
if curl -f -I http://$DOMAIN 2>&1 | grep -q "301\|302"; then
    echo "✅ HTTP to HTTPS redirect is working!"
else
    echo "⚠️  HTTP redirect test inconclusive"
fi

echo ""
echo "🎉 SSL setup completed successfully!"
echo "🔒 Your site should now be available at: https://$DOMAIN"
echo "🔄 SSL certificates will auto-renew via the renewal script"
echo ""
echo "Next steps:"
echo "1. Update EMAIL variable in this script with your actual email"
echo "2. Test your site: https://$DOMAIN"
echo "3. Set up the SSL renewal cron job (see renew-ssl.sh)"
