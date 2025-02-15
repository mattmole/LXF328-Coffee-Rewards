# Generated by Django 5.1.5 on 2025-01-26 20:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferenceType', models.CharField(choices=[('d', 'Drink'), ('f', 'Food')], max_length=1)),
                ('preferenceValue', models.CharField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.userprofile')),
            ],
        ),
    ]
