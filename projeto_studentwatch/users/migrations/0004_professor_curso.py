# Generated by Django 3.2.7 on 2021-11-01 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_presenca_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor_curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.curso')),
                ('professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.professorprofile')),
            ],
        ),
    ]
