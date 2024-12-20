# Generated by Django 4.1.10 on 2024-11-06 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_basitcalismaaudiorecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsitselZeminAudioRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('module_name', models.CharField(max_length=100)),
                ('audio_file', models.FileField(upload_to='isitsel_zemin_audio_records/')),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
