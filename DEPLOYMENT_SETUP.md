# Lineup Server Deployment Setup Guide

## Configuration Complete

The following files have been created:
- **Systemd Service**: `/etc/systemd/system/lineup.service`
- **Nginx Config**: `/etc/nginx/sites-available/rnblineup.hardapps.top`

## Step 1: Prepare the Application

```bash
cd /root/lineup

# Create a dedicated user (if not using www-data)
# sudo useradd -r -s /bin/bash lineup

# Ensure the venv exists
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create/migrate database
python manage.py migrate

# Exit venv
deactivate
```

## Step 2: Set Up SSL with Let's Encrypt

```bash
# Install certbot and nginx plugin
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate (this will auto-update your nginx config)
sudo certbot --nginx -d rnblineup.hardapps.top

# Auto-renewal setup (usually already enabled)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Step 3: Enable and Start Services

```bash
# Reload systemd daemon
sudo systemctl daemon-reload

# Enable lineup service to start on boot
sudo systemctl enable lineup

# Start the lineup service
sudo systemctl start lineup

# Check service status
sudo systemctl status lineup

# View service logs
sudo journalctl -u lineup -f
```

## Step 4: Configure Nginx

```bash
# Reload nginx to apply configuration
sudo systemctl reload nginx

# Verify nginx status
sudo systemctl status nginx

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Step 5: Update Django Settings (Important!)

Edit `/root/lineup/rnb_project/settings.py` and set:

```python
DEBUG = False  # Never run with DEBUG=True in production
SECRET_KEY = 'your-secure-random-secret-key-here'  # Change to a secure key
ALLOWED_HOSTS = ['rnblineup.hardapps.top']
```

You can set these via environment variables instead:
```bash
export DEBUG=False
export SECRET_KEY='your-secure-random-secret-key-here'
export ALLOWED_HOSTS='rnblineup.hardapps.top'
```

## Step 6: Enable Environment Variables for Systemd

Edit `/etc/systemd/system/lineup.service` and add your environment variables in the `[Service]` section:

```ini
[Service]
...
Environment="DEBUG=False"
Environment="SECRET_KEY=your-secure-random-secret-key-here"
...
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart lineup
```

## Verification

1. **Check service is running**:
   ```bash
   sudo systemctl status lineup
   ```

2. **Check the port is listening**:
   ```bash
   sudo netstat -tlnp | grep 5001
   ```

3. **Test nginx reverse proxy**:
   ```bash
   curl -I https://rnblineup.hardapps.top
   ```

4. **View live logs**:
   ```bash
   sudo journalctl -u lineup -f
   ```

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u lineup -n 50  # View last 50 lines of logs
sudo systemctl status lineup      # Check status
```

### Nginx errors
```bash
sudo nginx -t                      # Test configuration
sudo systemctl restart nginx       # Restart nginx
sudo tail -f /var/log/nginx/error.log
```

### SSL certificate renewal issues
```bash
sudo certbot renew --dry-run      # Test renewal
sudo certbot renew                # Force renewal if needed
sudo systemctl reload nginx       # Reload after renewal
```

### Permission issues
Ensure `/root/lineup` is readable by `www-data`:
```bash
sudo chown -R www-data:www-data /root/lineup
sudo chmod -R 755 /root/lineup
```

## SSL Auto-Renewal

Your SSL certificate will auto-renew 30 days before expiration via:
```bash
sudo systemctl enable certbot.timer
sudo systemctl list-timers certbot.timer
```

## Monitoring

Monitor your application with:
```bash
# Watch service logs
sudo journalctl -u lineup -f

# Watch access logs
sudo tail -f /var/log/nginx/access.log

# Watch error logs
sudo tail -f /var/log/nginx/error.log

# Check resource usage
top -p $(pgrep -f daphne)
```

## Security Checklist

- [ ] Set `DEBUG = False`
- [ ] Set a strong `SECRET_KEY`
- [ ] Update `ALLOWED_HOSTS`
- [ ] SSL certificate is active
- [ ] File permissions are correct (755 for dirs, 644 for files)
- [ ] Only necessary ports are open (80, 443)
- [ ] Database backups are configured
- [ ] Logs are monitored
- [ ] Static files are collected with `collectstatic`

## Rollback

To temporarily disable:
```bash
sudo systemctl stop lineup
sudo systemctl stop nginx
```

To re-enable:
```bash
sudo systemctl start lineup
sudo systemctl start nginx
```
