# Generated by Django 3.1.3 on 2020-11-21 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0002_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='prescribed_doc_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
