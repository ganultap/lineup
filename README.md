# Lineup - Django Edition

## 🎵 Lineup

A fun, modern Django web application for managing performance queues at Rhythm N Boost events!

### ✨ Features

- **Participant Page**: Easy queue joining with "Raise Hand" functionality
- **Host Control Panel**: Manage the queue with next/clear controls
- **Real-time Updates**: Queue updates every 2 seconds
- **Modern UI**: Vibrant gradients, animations, and glass-morphism effects
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile
- **Queue Persistence**: Uses Django database (SQLite by default)
- **Admin Panel**: Full Django admin for managing sessions and participants

### 🚀 Installation

1. **Clone or navigate to the project**:
   ```bash
   cd rnb_project
   ```

2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin panel)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Open in your browser**:
   - Participant page: `http://localhost:8000`
   - Host panel: `http://localhost:8000/host/`
   - Admin panel: `http://localhost:8000/admin/`

### 📁 Project Structure

```
rnb_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── rnb_project/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── lineup/                   # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # Request handlers
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   ├── consumers.py         # WebSocket consumers
│   ├── routing.py           # WebSocket routing
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── participant.html
│   │   └── host.html
│   └── static/
│       └── css/
│           └── style.css    # All styling
└── db.sqlite3               # SQLite database
```

### 🎨 Customization

You can customize:
- **Colors**: Edit CSS variables in `lineup/static/css/style.css` (`:root` section)
- **Session name**: Modify in `views.py` or admin panel
- **Queue refresh rate**: Change the `setInterval` value in templates (currently 2000ms)

### 🔧 API Endpoints

- `POST /api/raise-hand/` - Add participant to queue
- `POST /api/next/` - Move to next participant
- `POST /api/clear/` - Clear entire queue
- `GET /api/queue/` - Get current queue
- `POST /api/remove/` - Remove a participant

### 📦 Deployment

For production, consider:
1. Using PostgreSQL instead of SQLite
2. Setting `DEBUG = False` in settings.py
3. Using a production ASGI server (Daphne, Uvicorn)
4. Setting up proper static file handling
5. Using environment variables for sensitive settings

### 🎉 Enjoy!

Have fun managing your Rhythm N Boost events! 🎵✨
