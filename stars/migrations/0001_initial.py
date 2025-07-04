# Generated by Django 5.2 on 2025-04-21 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constellations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ra', models.FloatField(help_text='Right Ascension (도 단위)')),
                ('dec', models.FloatField(help_text='Declination (도 단위)')),
                ('magnitude', models.FloatField(blank=True, help_text='시등급 (밝기)', null=True)),
                ('spectral_type', models.CharField(blank=True, max_length=10, null=True)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('is_custom', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('constellation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='constellations.constellation')),
            ],
        ),
    ]
