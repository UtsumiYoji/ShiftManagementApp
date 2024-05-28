# Generated by Django 4.2.13 on 2024-05-24 00:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('place_name', models.CharField(blank=True, help_text='If your store is inside of mall or something', max_length=255, null=True)),
                ('address1', models.CharField(blank=True, help_text='Street name', max_length=255, null=True, verbose_name='adress1')),
                ('address2', models.CharField(blank=True, help_text='(Optional) building name', max_length=255, null=True, verbose_name='adress2')),
                ('city', models.CharField(blank=True, help_text='or Town', max_length=255, null=True, verbose_name='city')),
                ('postal_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='postal code')),
                ('province', models.CharField(blank=True, max_length=255, null=True, verbose_name='province')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=255, verbose_name='field')),
                ('before', models.CharField(max_length=255, verbose_name='before')),
                ('after', models.CharField(max_length=255, verbose_name='after')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('editor_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stores')),
            ],
        ),
        migrations.CreateModel(
            name='ShiftManagers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stores')),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('store_object', 'user_object')},
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stores')),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('store_object', 'user_object')},
            },
        ),
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('start_at', models.TimeField(blank=True, null=True)),
                ('finish_at', models.TimeField(blank=True, null=True)),
                ('store_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stores')),
            ],
            options={
                'unique_together': {('store_object', 'day')},
            },
        ),
    ]
