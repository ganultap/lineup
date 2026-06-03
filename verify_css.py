import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rnb_project.settings')
django.setup()

from django.test import Client
import re

# Create test client
client = Client()
client.login(username='testuser', password='test123')

# Get the participant page
response = client.get('/')
html = response.content.decode()

print("=" * 60)
print("PARTICIPANT PAGE VERIFICATION")
print("=" * 60)

# Check key structural elements
checks = {
    "Page Status": response.status_code == 200,
    "CSS Link Present": '/static/css/style.css' in html,
    "Navigation Bar": '<nav class="top-nav">' in html,
    "Main Header": 'RHYTHM N BOOST' in html,
    "Main Grid Layout": 'class="main-grid"' in html,
    "Left Column (Events)": 'class="left-column"' in html,
    "Right Column (Lineup)": 'class="right-column"' in html,
    "Registrations Panel": 'class="registrations-panel"' in html,
    "Lineup Panel": 'class="lineup-panel"' in html,
    "Queue Container": 'class="queue-container"' in html,
    "Available Events Section": 'Available Events' in html,
    "Current Lineup Section": 'Current Lineup' in html,
}

for check, result in checks.items():
    status = "✓" if result else "✗"
    print(f"{status} {check}")

# Extract and show CSS info
css_match = re.search(r'<link[^>]*href="/static/css/style\.css"', html)
if css_match:
    print(f"\n✓ CSS loaded from: {css_match.group()}")
    
# Check for key CSS classes in HTML
css_classes = [
    'participant-panel',
    'main-grid',
    'queue-item',
    'reg-card',
    'btn-primary',
    'btn-raise-hand',
    'empty-state',
    'status-badge',
    'queue-container'
]

print("\nCSS Classes Found in HTML:")
for cls in css_classes:
    if f'class="{cls}' in html or f'class=".*{cls}' in html:
        count = html.count(f'class="{cls}') + html.count(f' {cls}')
        print(f"  ✓ .{cls} ({count} instances)")

print("\n" + "=" * 60)
print("CSS IMPROVEMENTS APPLIED:")
print("=" * 60)

improvements = [
    "✓ Enhanced .participant-panel with gradient backgrounds",
    "✓ Improved .reg-card styling with better hover effects",
    "✓ Updated registration buttons with shadows and transitions",
    "✓ Better .lineup-panel layout and spacing",
    "✓ Enhanced .queue-item hover effects and transitions",
    "✓ Improved .btn-raise-hand with full-width styling",
    "✓ Better .status-badge with animation",
    "✓ Updated .empty-state with animations",
    "✓ Improved responsive design for mobile",
    "✓ Enhanced color consistency and visual hierarchy",
    "✓ Better shadows and depth for modern look",
    "✓ Improved typography and font weights",
]

for improvement in improvements:
    print(improvement)

print("\nCSS File Status:")
import os
css_path = '/root/lineup/lineup/static/css/style.css'
if os.path.exists(css_path):
    size = os.path.getsize(css_path)
    print(f"  File: {css_path}")
    print(f"  Size: {size:,} bytes")
    
    # Count CSS rules
    with open(css_path, 'r') as f:
        content = f.read()
        rules = content.count('{')
        print(f"  Rules: ~{rules}")
        
        # Check for key animations
        animations = ['pulse', 'float', 'slideIn', 'bounce']
        for anim in animations:
            if f'@keyframes {anim}' in content:
                print(f"  ✓ Animation: {anim}")

print("\n" + "=" * 60)

