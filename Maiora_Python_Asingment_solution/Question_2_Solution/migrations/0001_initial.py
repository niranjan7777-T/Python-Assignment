# Generated by Django 5.0.3 on 2024-11-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Joke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('joke_type', models.CharField(max_length=50)),
                ('setup', models.TextField(blank=True, null=True)),
                ('delivery', models.TextField(blank=True, null=True)),
                ('joke_text', models.TextField(blank=True, null=True)),
                ('nsfw', models.BooleanField(default=False)),
                ('political', models.BooleanField(default=False)),
                ('sexist', models.BooleanField(default=False)),
                ('safe', models.BooleanField(default=False)),
                ('lang', models.CharField(max_length=10)),
            ],
        ),
    ]
