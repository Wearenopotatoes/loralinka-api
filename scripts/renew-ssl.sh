#!/bin/bash

# SSL Certificate Renewal Script for LoraLink API
# This script handles automatic renewal of Let's Encrypt certificates

set -e  # Exit on any error

DOMAIN="api.loralink.live"
DEPLOY_PATH="/opt/loralinka-api"
LOG_FILE="/var/log/ssl-renewal.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log_message "Starting SSL certificate renewal check for $DOMAIN"

# Change to deployment directory
cd "$DEPLOY_PATH"

# Check if certificates need renewal (30 days before expiry)
if certbot certificates 2>/dev/null | grep -q "$DOMAIN"; then
    log_message "Certificate for $DOMAIN found, checking if renewal is needed..."

    # Attempt renewal (certbot only renews if < 30 days remain)
    if certbot renew --quiet --webroot -w ./certbot; then
        log_message "Certificate renewal check completed"

        # Check if certificate was actually renewed
        if certbot certificates 2>/dev/null | grep -A5 "$DOMAIN" | grep -q "VALID: $(date +%Y-%m-%d)"; then
            log_message "Certificate was renewed, restarting nginx..."

            # Restart nginx to load new certificate
            if docker compose restart nginx; then
                log_message "✅ Nginx restarted successfully"

                # Test the renewed certificate
                if curl -f -I https://$DOMAIN >/dev/null 2>&1; then
                    log_message "✅ HTTPS test successful after renewal"
                else
                    log_message "⚠️  HTTPS test failed after renewal"
                fi
            else
                log_message "❌ Failed to restart nginx"
                exit 1
            fi
        else
            log_message "No renewal was needed (certificate still valid for >30 days)"
        fi
    else
        log_message "❌ Certificate renewal failed"
        exit 1
    fi
else
    log_message "⚠️  No certificate found for $DOMAIN"
    exit 1
fi

log_message "SSL renewal process completed"