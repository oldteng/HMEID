# Generated by Django 2.1.2 on 2021-05-23 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_ld_snp'),
    ]

    operations = [
        migrations.AddField(
            model_name='sites',
            name='assess',
            field=models.PositiveIntegerField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sites',
            name='lp',
            field=models.PositiveIntegerField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sites',
            name='rp',
            field=models.PositiveIntegerField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sites',
            name='sr',
            field=models.PositiveIntegerField(default='null'),
            preserve_default=False,
        ),
    ]
