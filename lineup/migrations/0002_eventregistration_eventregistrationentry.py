from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='created_registrations',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistrationEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('registration', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='entries',
                    to='lineup.eventregistration',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='event_registrations',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['registered_at'],
                'unique_together': {('registration', 'user')},
            },
        ),
    ]
