# Generated by Django 5.0.4 on 2024-05-03 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chambre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('taille', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(blank=True, upload_to='chambres/')),
            ],
            options={
                'db_table': 'chambres',
            },
        ),
    ]