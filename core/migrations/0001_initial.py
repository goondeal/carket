# Generated by Django 4.1.7 on 2023-05-23 18:20

import core.services
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0002_city_name_ar_city_name_en_country_currency_ar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.CharField(max_length=31)),
                ('state', models.CharField(max_length=31)),
                ('slug', models.SlugField(allow_unicode=True, editable=False, max_length=127, unique=True)),
                ('description', models.CharField(max_length=511)),
                ('year', models.PositiveIntegerField()),
                ('mileage', models.PositiveIntegerField()),
                ('engine_cc', models.PositiveIntegerField()),
                ('transmission', models.CharField(max_length=31)),
                ('transmission_en', models.CharField(max_length=31, null=True)),
                ('transmission_ar', models.CharField(max_length=31, null=True)),
                ('body_type', models.CharField(max_length=31)),
                ('body_type_en', models.CharField(max_length=31, null=True)),
                ('body_type_ar', models.CharField(max_length=31, null=True)),
                ('fuel_type', models.CharField(max_length=31)),
                ('fuel_type_en', models.CharField(max_length=31, null=True)),
                ('fuel_type_ar', models.CharField(max_length=31, null=True)),
                ('color_name', models.CharField(max_length=31)),
                ('color_name_en', models.CharField(max_length=31, null=True)),
                ('color_name_ar', models.CharField(max_length=31, null=True)),
                ('color_hex', models.CharField(max_length=7)),
                ('interior_color_name', models.CharField(max_length=31, null=True)),
                ('interior_color_name_en', models.CharField(max_length=31, null=True)),
                ('interior_color_name_ar', models.CharField(max_length=31, null=True)),
                ('price', models.PositiveIntegerField()),
                ('price_currency', models.CharField(max_length=31)),
                ('price_currency_en', models.CharField(max_length=31, null=True)),
                ('price_currency_ar', models.CharField(max_length=31, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='CarBodyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('name_en', models.CharField(max_length=15, null=True)),
                ('name_ar', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('hex_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='CarDrivetrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarFeatureCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='CarFuelType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('year', models.PositiveIntegerField(null=True)),
                ('logo', models.ImageField(null=True, upload_to='images/makes_logos/')),
            ],
        ),
        migrations.CreateModel(
            name='CarMakeCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('flag_img', models.ImageField(upload_to='images/countries_flags/')),
            ],
        ),
        migrations.CreateModel(
            name='CarStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('is_available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CarTransmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=63, null=True)),
                ('phone1', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('phone2', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('name_en', models.CharField(max_length=63, null=True)),
                ('name_ar', models.CharField(max_length=63, null=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carmake')),
            ],
        ),
        migrations.AddField(
            model_name='carmake',
            name='country_of_origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.carmakecountry'),
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=core.services.get_car_image_upload_path)),
                ('order', models.PositiveSmallIntegerField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.car')),
            ],
        ),
        migrations.CreateModel(
            name='CarFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('name_en', models.CharField(max_length=31, null=True)),
                ('name_ar', models.CharField(max_length=31, null=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carfeaturecategory')),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.contact'),
        ),
        migrations.AddField(
            model_name='car',
            name='features',
            field=models.ManyToManyField(to='core.carfeature'),
        ),
        migrations.AddField(
            model_name='car',
            name='interested_users',
            field=models.ManyToManyField(related_name='cars_list', through='core.CarsList', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.carmodel'),
        ),
        migrations.AddField(
            model_name='car',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.carstatus'),
        ),
        migrations.AddField(
            model_name='car',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_cars', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='car',
            name='wishlist_users',
            field=models.ManyToManyField(related_name='saved_cars', through='core.Wishlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='wishlist',
            constraint=models.UniqueConstraint(fields=('user', 'car'), name='no_repeated_cars_in_user_wishlist'),
        ),
        migrations.AddConstraint(
            model_name='carslist',
            constraint=models.UniqueConstraint(fields=('user', 'car'), name='no_repeated_cars_in_user_cars_list'),
        ),
        migrations.AddConstraint(
            model_name='carmodel',
            constraint=models.UniqueConstraint(fields=('make', 'name'), name='no_repeated_models_for_make'),
        ),
        migrations.AddConstraint(
            model_name='carfeature',
            constraint=models.UniqueConstraint(fields=('category', 'name'), name='no_repeated_features_for_category'),
        ),
        migrations.AddIndex(
            model_name='car',
            index=models.Index(fields=['country', 'state'], name='core_car_country_8c2809_idx'),
        ),
    ]
