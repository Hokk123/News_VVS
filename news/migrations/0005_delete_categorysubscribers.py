# Generated by Django 4.1 on 2022-10-15 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_category_subscribers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategorySubscribers',
        ),
    ]
