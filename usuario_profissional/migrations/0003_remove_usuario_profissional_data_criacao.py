# Generated by Django 3.1.4 on 2020-12-02 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario_profissional', '0002_usuario_profissional_data_criacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario_profissional',
            name='data_criacao',
        ),
    ]