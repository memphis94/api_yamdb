# Generated by Django 2.2.16 on 2022-09-12 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220912_2115'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('id',)},
        ),
    ]
