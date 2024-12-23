# Generated by Django 4.1.10 on 2024-11-06 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_alter_karmasikcalismaclickrecord_video_file_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='KarmasikCalismaAudioRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('module', models.CharField(default='karmaşik_calisma', max_length=255)),
                ('audio_file', models.FileField(upload_to='karmasik_calisma_audio/')),
                ('recorded_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
