# Generated by Django 3.0 on 2019-12-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20191207_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='page_count',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='word_count',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='readingrecord',
            name='finish_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='readingrecord',
            name='read_page_count',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='readingrecord',
            name='read_word_count',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='readingrecord',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
