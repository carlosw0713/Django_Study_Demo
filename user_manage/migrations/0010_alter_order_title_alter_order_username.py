# Generated by Django 4.2 on 2023-04-27 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0009_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='title',
            field=models.CharField(max_length=64, unique=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='order',
            name='username',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='user_manage.admin', verbose_name='购买用户'),
        ),
    ]
