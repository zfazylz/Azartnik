# Generated by Django 2.1.4 on 2018-12-04 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainGameApp', '0002_auto_20181204_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbet',
            name='side',
            field=models.IntegerField(default=-1, null=True),
        ),
    ]