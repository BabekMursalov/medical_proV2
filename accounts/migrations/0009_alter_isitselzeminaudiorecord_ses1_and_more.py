# Generated by Django 4.1.10 on 2024-11-06 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_isitselzeminaudiorecord_ses1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses1',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses10',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses2',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses3',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses4',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses5',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses6',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses7',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses8',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
        migrations.AlterField(
            model_name='isitselzeminaudiorecord',
            name='ses9',
            field=models.FileField(blank=True, null=True, upload_to='isitsel_zemin_audio_records/'),
        ),
    ]