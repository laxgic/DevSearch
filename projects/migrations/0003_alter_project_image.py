# Generated by Django 3.2.9 on 2021-12-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
