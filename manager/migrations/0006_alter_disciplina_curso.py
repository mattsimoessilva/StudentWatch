# Generated by Django 3.2.7 on 2021-11-26 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20211123_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='curso',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.curso'),
        ),
    ]
