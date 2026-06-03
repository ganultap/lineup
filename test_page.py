import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rnb_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

# Create a test user
user, created = User.objects.get_or_create(username='testuser', defaults={})
if created:
    user.set_password('test123')
    user.save()
    print(f"Created test user: {user.username}")
else:
    print(f"Test user already exists: {user.username}")

# Test the page loads
client = Client()
client.login(username='testuser', password='test123')
response = client.get('/')
print(f"\nIndex page status: {response.status_code}")

# Check for CSS link
html = response.content.decode()
if 'style.css' in html:
    print("✓ CSS link found in HTML")
if 'RHYTHM N BOOST' in html:
    print("✓ Header found")
if 'Available Events' in html or 'registrationCards' in html:
    print("✓ Registrations panel found")
if 'Current Lineup' in html or 'queueList' in html:
    print("✓ Lineup panel found")
    
# Print snippet
print("\nHTML head section (first 1000 chars):")
if '<head>' in html:
    start = html.index('<head>')
    end = html.index('</head>') + 7
    print(html[start:min(start+800, end)])

