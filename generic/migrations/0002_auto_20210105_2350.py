# Generated by Django 3.1.4 on 2021-01-05 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='picture',
            field=models.ImageField(blank=True, default='static/images/default.png', help_text='1:1 aspect ratio required.', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='picture',
            field=models.ImageField(blank=True, default='static/images/default.png', help_text='1:1 aspect ratio required.', null=True, upload_to=''),
        ),
    ]