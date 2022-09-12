# Generated by Django 2.2.16 on 2022-09-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220912_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('pub_date',), 'verbose_name': 'Ревью', 'verbose_name_plural': 'Ревью'},
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_review'),
        ),
    ]
