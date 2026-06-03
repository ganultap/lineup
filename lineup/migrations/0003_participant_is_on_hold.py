from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lineup', '0002_eventregistration_eventregistrationentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='is_on_hold',
            field=models.BooleanField(default=False),
        ),
    ]
