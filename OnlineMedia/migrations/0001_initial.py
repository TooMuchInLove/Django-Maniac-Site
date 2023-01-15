# Generated by Django 3.0.2 on 2020-06-22 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_header', models.CharField(max_length=50, unique=True, verbose_name='Краткая статья')),
                ('news_text', models.TextField(unique=True, verbose_name='Текст новости')),
                ('news_date', models.DateField(verbose_name='Дата новости')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(help_text='Название раздела', max_length=80, unique=True, verbose_name='Раздел')),
                ('section_name_eng', models.CharField(default='name', help_text='Название раздела', max_length=80, verbose_name='Раздел на инглише')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
                ('tag_desc', models.CharField(max_length=255, verbose_name='Описание тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(help_text='Заголовок статьи', max_length=80, verbose_name='Заголовок')),
                ('preview_text', models.TextField(help_text='Краткое описание', max_length=300, verbose_name='Краткое описание')),
                ('preview_img', models.ImageField(help_text='Картинка для статьи в списке', upload_to='', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Полный текст статьи', max_length=10000, verbose_name='Текст')),
                ('create_date', models.DateField(help_text='Дата написания статьи', verbose_name='Дата')),
                ('create_time', models.TimeField(help_text='Время написания статьи', verbose_name='Время')),
                ('views', models.IntegerField(default=0, help_text='Просмотры')),
                ('id_project', models.ForeignKey(help_text='Идентификатор проекта', on_delete=django.db.models.deletion.CASCADE, to='account.Project', verbose_name='Проект')),
                ('id_section', models.ForeignKey(help_text='Идентификатор категории', on_delete=django.db.models.deletion.CASCADE, to='OnlineMedia.Section', verbose_name='Категория')),
                ('tag', models.ManyToManyField(to='OnlineMedia.Tag')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]