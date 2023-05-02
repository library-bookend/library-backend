# Generated by Django 4.0.7 on 2023-05-02 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('genre', models.CharField(choices=[('Fantasy', 'Fantasy'), ('Romance', 'Romance'), ('Science Fiction', 'Science Fiction'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Adventure', 'Adventure'), ('Biography', 'Biography'), ('Classics', 'Classics'), ('Drama', 'Drama'), ('Family', 'Family'), ('History', 'History'), ('History Fiction', 'History Fiction'), ('Literary Fiction', 'Literary Fiction'), ('Musical', 'Musical'), ('Religion', 'Religion'), ('Satire', 'Satire'), ('Society', 'Society'), ('Thriller', 'Thriller'), ('Western', 'Western'), ('Undefined', 'Undefined')], default='Undefined', max_length=50)),
                ('pages', models.IntegerField()),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('copies_amount', models.IntegerField()),
                ('book_cover', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
    ]
