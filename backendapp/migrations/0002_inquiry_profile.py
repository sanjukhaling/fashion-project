# Generated by Django 5.1.3 on 2024-11-10 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('qualification', models.CharField(blank=True, max_length=200, null=True)),
                ('post', models.CharField(max_length=100)),
            ],
        ),
    ]
