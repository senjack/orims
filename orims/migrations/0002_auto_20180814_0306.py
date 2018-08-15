# Generated by Django 2.0.2 on 2018-08-14 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orims', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceunit',
            name='unit_cover_photo',
            field=models.FileField(max_length=500, upload_to='photos/uploads/ServiceUnit/cover_photos'),
        ),
        migrations.AlterField(
            model_name='serviceunit',
            name='unit_featured_image',
            field=models.FileField(max_length=500, upload_to='photos/uploads/ServiceUnit/featured_images'),
        ),
        migrations.AlterField(
            model_name='serviceunit',
            name='unit_logo',
            field=models.FileField(max_length=500, upload_to='photos/uploads/ServiceUnit/logos'),
        ),
        migrations.AlterField(
            model_name='serviceunit',
            name='unit_name',
            field=models.CharField(max_length=200, verbose_name='Service Unit name'),
        ),
        migrations.AlterField(
            model_name='serviceunit',
            name='unit_type',
            field=models.CharField(choices=[('select', 'Select Type of service unit'), ('Ministry', 'Ministry'), ('Organization', 'Organization'), ('Firm', 'Firm'), ('Other', 'Others')], default='select', max_length=15, verbose_name='Service Unit type'),
        ),
    ]
