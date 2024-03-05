# Generated by Django 5.0.2 on 2024-03-05 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductsApp', '0003_remove_productimage_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='liked_products', to=settings.AUTH_USER_MODEL),
        ),
    ]
