# 🔒 SSL Automation Guide

This repository now includes full SSL automation for the LoraLink API using Let's Encrypt certificates.

## 🚀 Quick Start

The SSL setup is now **fully automated** through GitHub Actions! On your first deployment:

1. **Add optional SSL_EMAIL secret** (recommended):
   ```
   Go to GitHub repo → Settings → Secrets → Actions
   Add: SSL_EMAIL = your-email@example.com
   ```

2. **Deploy normally**:
   ```bash
   git push origin master
   ```

3. **That's it!** SSL will be automatically set up on first deployment.

## 📁 New Files Added

| File | Description |
|------|-------------|
| `scripts/init-ssl.sh` | Automated SSL certificate setup script |
| `scripts/renew-ssl.sh` | SSL certificate renewal script |
| `SSL-AUTOMATION.md` | This documentation file |

## 🔧 How It Works

### First Deployment
1. **HTTP-only setup**: Starts with temporary nginx config for certificate validation
2. **Certificate request**: Uses certbot to get Let's Encrypt certificate
3. **SSL config**: Switches to final nginx config with HTTPS + HTTP redirect
4. **Auto-renewal**: Sets up cron job for automatic certificate renewal

### Subsequent Deployments
- Skips SSL setup if certificate already exists
- Ensures renewal cron job is installed
- Normal deployment continues

## 📋 Manual Commands (if needed)

### Manual SSL Setup
```bash
cd /opt/loralinka-api
bash scripts/init-ssl.sh
```

### Manual Certificate Renewal
```bash
cd /opt/loralinka-api
bash scripts/renew-ssl.sh
```

### Check Certificate Status
```bash
certbot certificates
```

### Check Renewal Cron Job
```bash
crontab -l | grep renew-ssl
```

## 🔍 Verification

After deployment, verify SSL is working:

```bash
# Test HTTPS
curl -I https://api.loralink.live

# Test HTTP redirect
curl -I http://api.loralink.live
```

## ⚙️ Configuration

### Domain Configuration
The domain `api.loralink.live` is hardcoded in:
- `scripts/init-ssl.sh`
- `scripts/renew-ssl.sh`
- `nginx/nginx.conf`

To change domain, update these files.

### Email Configuration
SSL certificate email is configured via:
1. GitHub secret `SSL_EMAIL` (recommended)
2. Or manually in `scripts/init-ssl.sh`

## 🔄 Certificate Renewal

Certificates automatically renew via cron job:
```
0 0,12 * * * cd /opt/loralinka-api && bash scripts/renew-ssl.sh
```

- Runs twice daily (00:00 and 12:00)
- Only renews if <30 days remain
- Logs to `/var/log/ssl-renewal.log`
- Automatically restarts nginx after renewal

## 🛠️ Troubleshooting

### SSL Setup Fails
1. Check domain DNS points to your server
2. Ensure port 80 is accessible
3. Verify containers are running: `docker compose ps`
4. Check logs: `docker compose logs nginx`

### Certificate Renewal Fails
1. Check renewal logs: `tail -f /var/log/ssl-renewal.log`
2. Test manual renewal: `bash scripts/renew-ssl.sh`
3. Verify cron job exists: `crontab -l`

### Domain Access Issues
1. Test HTTP first: `curl -I http://api.loralink.live`
2. Check nginx config: `docker compose exec nginx nginx -t`
3. Restart services: `docker compose restart`

## 📊 GitHub Secrets

| Secret | Required | Description |
|--------|----------|-------------|
| `SSH_PRIVATE_KEY` | ✅ Yes | SSH private key for server access |
| `SERVER_HOST` | ✅ Yes | Server IP or domain |
| `SSH_USER` | ✅ Yes | SSH username |
| `DEPLOY_PATH` | ✅ Yes | Deployment directory path |
| `API_KEY` | ✅ Yes | Production API key |
| `DATABASE_URL` | ✅ Yes | Production database URL |
| `SSL_EMAIL` | 📧 Optional | Email for SSL certificates (recommended) |

## ✅ Success Indicators

After successful SSL automation:

- ✅ HTTPS site accessible: `https://api.loralink.live`
- ✅ HTTP redirects to HTTPS
- ✅ SSL certificate valid for 90 days
- ✅ Auto-renewal cron job installed
- ✅ Nginx configured with proper SSL settings