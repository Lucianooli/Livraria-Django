# Generated by Django 5.1.1 on 2024-09-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib_shop', '0003_alter_livro_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='sinopse',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='livro',
            name='descricao',
            field=models.TextField(default=''),
        ),
    ]
