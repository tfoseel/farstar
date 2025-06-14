# Generated by Django 5.2 on 2025-04-21 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('connections', models.JSONField(blank=True, help_text='별들 간 연결 (Star ID 쌍 목록)', null=True)),
            ],
        ),
    ]
