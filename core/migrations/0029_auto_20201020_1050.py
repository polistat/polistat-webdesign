# Generated by Django 2.1.3 on 2020-10-20 14:50

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_featured_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
