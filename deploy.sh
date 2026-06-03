#!/bin/bash
set -e

echo "🚀 Lineup Deployment Setup"
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DOMAIN="rnblineup.hardapps.top"
PORT="5001"
APP_DIR="/root/lineup"

echo -e "${YELLOW}Step 1: Preparing Python environment...${NC}"
cd "$APP_DIR"
python3 -m venv venv || echo "venv already exists"
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
deactivate

echo -e "${GREEN}✓ Python environment ready${NC}"

echo -e "${YELLOW}Step 2: Collecting static files...${NC}"
source venv/bin/activate
python manage.py collectstatic --noinput
deactivate

echo -e "${GREEN}✓ Static files collected${NC}"

echo -e "${YELLOW}Step 3: Running database migrations...${NC}"
source venv/bin/activate
python manage.py migrate
deactivate

echo -e "${GREEN}✓ Database migrations complete${NC}"

echo -e "${YELLOW}Step 4: Setting up systemd service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable lineup
echo -e "${GREEN}✓ Systemd service configured${NC}"

echo -e "${YELLOW}Step 5: Configuring nginx...${NC}"
sudo systemctl reload nginx || sudo systemctl restart nginx
echo -e "${GREEN}✓ Nginx configured${NC}"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Next steps:"
echo "1. Update Django settings: vi $APP_DIR/rnb_project/settings.py"
echo "2. Set production DEBUG=False and SECRET_KEY"
echo "3. Setup SSL: sudo certbot --nginx -d $DOMAIN"
echo "4. Start service: sudo systemctl start lineup"
echo "5. Check status: sudo systemctl status lineup"
echo "6. View logs: sudo journalctl -u lineup -f"
echo ""
echo "For detailed instructions, see: $APP_DIR/DEPLOYMENT_SETUP.md"
