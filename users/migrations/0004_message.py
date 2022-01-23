# Generated by Django 3.2.9 on 2022-01-23 10:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211218_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipient_profile', to='users.profile')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender_profile', to='users.profile')),
            ],
            options={
                'ordering': ['is_read', '-created'],
            },
        ),
    ]