# 🚀 Deployment Guide

This project uses GitHub Actions for automatic deployment to your server via SCP (no Docker registry needed).

## GitHub Secrets Setup

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add these secrets:

### Required Secrets

| Secret Name | Description | Example |
|------------|-------------|---------|
| `SSH_PRIVATE_KEY` | Your private SSH key for server access | `-----BEGIN OPENSSH PRIVATE KEY-----` |
| `SERVER_HOST` | Server IP address or domain | `192.168.1.100` or `api.yourdomain.com` |
| `SSH_USER` | SSH username on the server | `root` or `ubuntu` |
| `DEPLOY_PATH` | Deployment directory on server | `/opt/loralinka-api` |
| `API_KEY` | Production API key | `prod-secret-key-here` |
| `DATABASE_URL` | Production database connection | `postgresql://user:pass@host:5432/db` |

## Server Preparation

1. **Create deployment directory:**
   ```bash
   sudo mkdir -p /opt/loralinka-api
   sudo chown $USER:$USER /opt/loralinka-api
   ```

2. **Verify Docker and Docker Compose are installed:**
   ```bash
   docker --version
   docker compose version
   ```

## SSH Key Setup

1. **Generate SSH key pair (if you don't have one):**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions"
   ```

2. **Add public key to server:**
   ```bash
   ssh-copy-id -i ~/.ssh/id_rsa.pub user@your-server
   ```

3. **Add private key to GitHub secrets:**
   Copy content of `~/.ssh/id_rsa` to `SSH_PRIVATE_KEY` secret

## Deployment Process

### Automatic Deployment
- Every push to `master` branch triggers automatic deployment
- Files are copied via SCP to your server
- Environment variables are created from GitHub secrets
- Docker containers are rebuilt and restarted

### Manual Deployment
Go to Actions tab → Deploy to Server → Run workflow

## What Happens During Deployment

1. ✅ Checkout code from repository
2. ✅ Setup SSH connection to server
3. ✅ Copy all project files via SCP
4. ✅ Create `.env` file with production secrets
5. ✅ Stop existing containers
6. ✅ Build and start new containers
7. ✅ Clean up unused Docker images

## Security Notes

- `.env` file is created with `600` permissions (owner read/write only)
- Environment variables are stored securely in GitHub secrets
- No credentials are exposed in the repository
- SSH connection uses key-based authentication

## Troubleshooting

### Deployment fails at SCP step
- Check `SSH_PRIVATE_KEY` format (include headers and footers)
- Verify `SSH_USER` has write permissions to `DEPLOY_PATH`

### Docker build fails
- SSH into server and check Docker daemon: `sudo systemctl status docker`
- Check container logs: `docker compose logs`

### Application not responding
- Check if containers are running: `docker compose ps`
- Check application logs: `docker compose logs api`
- Verify `.env` file was created correctly