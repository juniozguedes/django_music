# Generated by Django 3.0.4 on 2020-03-11 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0002_auto_20200308_2252'),
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artists.Artist'),
        ),
    ]
