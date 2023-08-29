from math import sin, cos, acos
from datetime import datetime

from django.db import models
from django.conf import settings
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField

from .services import get_car_image_upload_path
from management.models import City


class CarMakeCountry(models.Model):
    name = models.CharField(max_length=31)
    flag_img = models.ImageField(upload_to='images/countries_flags/')

    def __str__(self) -> str:
        return self.name


class CarMake(models.Model):
    name = models.CharField(max_length=31)
    year = models.PositiveIntegerField(null=True)
    country_of_origin = models.ForeignKey(
        CarMakeCountry, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='images/makes_logos/', null=True)

    def __str__(self) -> str:
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=63)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name}|{self.make}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['make', 'name'], name='no_repeated_models_for_make')
        ]


class CarBodyType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name


class CarColor(models.Model):
    name = models.CharField(max_length=31)
    hex_code = models.CharField(max_length=7)

    def __str__(self) -> str:
        return self.name


class CarDrivetrain(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self) -> str:
        return self.name


class CarFuelType(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self) -> str:
        return self.name


class CarTransmission(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self) -> str:
        return self.name


class CarFeatureCategory(models.Model):
    name = models.CharField(max_length=31)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)

    def __str__(self) -> str:
        return self.name


class CarFeature(models.Model):
    name = models.CharField(max_length=31)
    category = models.ForeignKey(CarFeatureCategory, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)

    def __str__(self) -> str:
        return f'{self.name}|{self.category.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'], name='no_repeated_features_for_category')
        ]


class CarStatus(models.Model):
    name = models.CharField(max_length=31)
    is_available = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name}'


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    street = models.CharField(max_length=63, null=True)
    phone1 = PhoneNumberField()
    phone2 = PhoneNumberField(null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self) -> str:
        return f'{self.phone1}'

    def acc_distance_to_user_location(self, user_location):
        lat1 = self.contact.lat
        lon1 = self.contact.lon

        if lon1 != None and lat1 != None:
            assert (len(user_location) == 2)
            user_lon, user_lat = user_location
            # (6371 is Earth radius in km.)
            return acos(sin(lat1) * sin(user_lat) + cos(lat1) * cos(user_lat) * cos(user_lon-lon1)) * 6371
        else:
            return None


class Car(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_cars',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT)
    country = models.CharField(max_length=31)
    state = models.CharField(max_length=31)

    slug = models.SlugField(unique=True, max_length=127,
                            allow_unicode=True, editable=False)
    description = models.CharField(max_length=511)
    status = models.ForeignKey(CarStatus, on_delete=models.PROTECT)

    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    engine_cc = models.PositiveIntegerField()
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    transmission = models.CharField(max_length=31)
    body_type = models.CharField(max_length=31)
    fuel_type = models.CharField(max_length=31)

    color_name = models.CharField(max_length=31)
    color_hex = models.CharField(max_length=7)
    interior_color_name = models.CharField(max_length=31, null=True)

    features = models.ManyToManyField(CarFeature)

    price = models.PositiveIntegerField()
    price_currency = models.CharField(max_length=31)

    interested_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='CarsList', related_name='cars_list')
    wishlist_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='Wishlist', related_name='saved_cars')

    class Meta:
        ordering = ('-created_at',)
        indexes = (
            models.Index(fields=('country', 'state')),
        )

    @property
    def name(self):
        return f'{self.model.make} {self.model.name} {self.year if self.year else ""}'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            time = str(datetime.now().timestamp()).split('.')[0][-5:-1]
            self.slug = slugify(
                f'{self.name}{self.user.id}{time}', allow_unicode=True)
            if len(self.slug) > 127:
                self.slug = self.slug[-127:]
        super(Car, self).save(*args, **kwargs)


class CarImage(models.Model):
    img = models.ImageField(upload_to='cars') #get_car_image_upload_path)
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveSmallIntegerField()


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'car'], name='no_repeated_cars_in_user_wishlist')
        ]


class CarsList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'car'], name='no_repeated_cars_in_user_cars_list')
        ]
