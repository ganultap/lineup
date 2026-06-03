# 🎉 Lineup Server Deployment - SUCCESS

## Deployment Completed: June 3, 2026

### ✅ What's Been Set Up

1. **Systemd Service** - Running Daphne on 127.0.0.1:5001
   - Auto-restarts on failure
   - Starts on boot
   - Runs as www-data user
   - Environment variables configured

2. **Nginx Reverse Proxy** - rnblineup.hardapps.top
   - HTTP (port 80) → HTTPS redirect
   - HTTPS (port 443) with HTTP/2
   - WebSocket support for Django Channels
   - Static file serving with caching
   - Security headers enabled (HSTS, CSP, etc.)

3. **SSL Certificate** - Let's Encrypt
   - Active for rnblineup.hardapps.top
   - Auto-renewal enabled (certbot timer)
   - Certificate path: `/etc/letsencrypt/live/rnblineup.hardapps.top/`

4. **Production Settings**
   - DEBUG=False
   - SECRET_KEY set (production-grade)
   - ALLOWED_HOSTS configured
   - Static files collected

---

## 🚀 Current Status

```
Service: lineup.service
Status: Active (running)
Port: 127.0.0.1:5001
PID: 3764995
Memory: 49.7M
```

```
Service: nginx
Status: Active (running)
Ports: 80 (HTTP), 443 (HTTPS)
Config: /etc/nginx/sites-enabled/rnblineup.hardapps.top
```

```
SSL Status: Active
Domain: rnblineup.hardapps.top
Certificate: Let's Encrypt
Renewal: Auto (30 days before expiry)
```

---

## 📊 Verification Tests Passed

✅ Daphne ASGI server listening on 127.0.0.1:5001
✅ Nginx reverse proxy operational
✅ HTTPS working with HTTP/2
✅ SSL certificate valid
✅ Security headers present (HSTS, X-Frame-Options, etc.)
✅ WebSocket support enabled
✅ Static files configured
✅ Database migrations applied

---

## 📝 Important Information

### Service Commands

```bash
# Check service status
sudo systemctl status lineup

# Start/stop/restart
sudo systemctl start lineup
sudo systemctl stop lineup
sudo systemctl restart lineup

# View logs in real-time
sudo journalctl -u lineup -f

# View last 50 lines of logs
sudo journalctl -u lineup -n 50

# Check if port is listening
sudo netstat -tlnp | grep 5001
```

### Nginx Commands

```bash
# Reload configuration
sudo systemctl reload nginx

# Restart service
sudo systemctl restart nginx

# Test configuration syntax
sudo nginx -t

# View access logs
sudo tail -f /var/log/nginx/access.log

# View error logs
sudo tail -f /var/log/nginx/error.log
```

### SSL Certificate

```bash
# View certificate details
sudo certbot certificates

# Test renewal (dry-run)
sudo certbot renew --dry-run

# Force renewal if needed
sudo certbot renew

# Check renewal timer
sudo systemctl list-timers certbot.timer
```

---

## 🔒 Security Configuration

All the following security best practices are enabled:

- ✅ HTTPS with TLS 1.2/1.3
- ✅ HTTP → HTTPS redirect
- ✅ HSTS (HTTP Strict-Transport-Security)
- ✅ X-Frame-Options: SAMEORIGIN
- ✅ X-Content-Type-Options: nosniff
- ✅ X-XSS-Protection: 1; mode=block
- ✅ Referrer-Policy: strict-origin-when-cross-origin
- ✅ DEBUG = False
- ✅ Strong SECRET_KEY
- ✅ Limited ALLOWED_HOSTS

---

## 📁 File Locations

| File | Path |
|------|------|
| Systemd Service | `/etc/systemd/system/lineup.service` |
| Nginx Config | `/etc/nginx/sites-enabled/rnblineup.hardapps.top` |
| Django App | `/root/lineup/` |
| Static Files | `/root/lineup/staticfiles/` |
| Database | `/root/lineup/db.sqlite3` |
| Logs (systemd) | `journalctl -u lineup` |
| Logs (Nginx Access) | `/var/log/nginx/access.log` |
| Logs (Nginx Error) | `/var/log/nginx/error.log` |
| SSL Cert | `/etc/letsencrypt/live/rnblineup.hardapps.top/` |
| Certbot Logs | `/var/log/letsencrypt/` |

---

## 🔧 Configuration Details

### Daphne (ASGI Server)
- **Command**: `/root/lineup/venv/bin/daphne -b 127.0.0.1 -p 5001 rnb_project.asgi:application`
- **User**: www-data
- **Port**: 5001 (localhost only)
- **Auto-restart**: On-failure (10s delay)

### Nginx Reverse Proxy
- **Server Block**: rnblineup.hardapps.top
- **Upstream**: 127.0.0.1:5001
- **WebSocket Support**: ✅ Enabled
- **Max Upload**: 20MB
- **Static Cache**: 30 days
- **Media Cache**: 7 days

### Django
- **Framework**: Django 4.2.7
- **ASGI**: Channels 4.0.0
- **Server**: Daphne 4.0.0
- **Static Storage**: WhiteNoise CompressedManifestStaticFilesStorage
- **Database**: SQLite3

---

## ⚠️ Important Notes

1. **Database**: Currently using SQLite3. For production with multiple workers, consider PostgreSQL.

2. **Static Files**: Already collected. Run `python manage.py collectstatic` if you make CSS/JS changes.

3. **Media Files**: Configure media directory path if needed in nginx config and Django settings.

4. **Environment Variables**: Set in `/etc/systemd/system/lineup.service`

5. **Backups**: Set up regular database backups (db.sqlite3)

6. **Monitoring**: Watch `/var/log/nginx/error.log` and `journalctl -u lineup` for issues.

---

## 🆘 Troubleshooting

### Service won't start
```bash
sudo journalctl -u lineup -n 50
sudo systemctl status lineup
```

### Nginx errors
```bash
sudo nginx -t  # Check syntax
sudo systemctl restart nginx
tail -f /var/log/nginx/error.log
```

### SSL issues
```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

### Permission denied
```bash
sudo chown -R www-data:www-data /root/lineup
sudo chmod -R 755 /root/lineup
```

---

## 📞 Support

For detailed deployment guide: See `DEPLOYMENT_SETUP.md`

For production improvements:
- Consider PostgreSQL instead of SQLite3
- Set up log rotation for `/var/log/nginx/`
- Configure backup strategy for database
- Monitor resource usage and set up alerting
- Consider load balancing for scaling

---

**Deployment Date**: June 3, 2026
**Domain**: rnblineup.hardapps.top
**Port**: 5001 (internal), 443 (external HTTPS)
