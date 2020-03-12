# Generated by Django 3.0.4 on 2020-03-11 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0004_auto_20200311_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.Album')),
            ],
        ),
    ]
