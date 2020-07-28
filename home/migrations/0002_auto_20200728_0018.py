# Generated by Django 3.0.7 on 2020-07-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trading',
            name='company_name',
            field=models.CharField(default='Company', max_length=30),
        ),
        migrations.AddField(
            model_name='trading',
            name='multiplicationfactor',
            field=models.PositiveIntegerField(default=1),
        ),
    ]