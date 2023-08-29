from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from django.core.exceptions import BadRequest

from management.models import City


def get_car_image_upload_path(instance, filename):
        '''
        used in models.CARIMAGE.img field
        [filename]: final name to be saved
        '''
        return f'images/cars/{instance.car.slug}/{filename}'


def get_filtered_cars(qs, params):
    unsafe_city_id = params.get('city', None)
    unsafe_min_price = params.get('min_price', None)
    unsafe_max_price = params.get('max_price', None)
    unsafe_min_year = params.get('min_year', None)
    unsafe_max_year = params.get('max_year', None)
    unsafe_mileage = params.get('mileage', None)
    unsafe_models = params.getlist('models', None)
    unsafe_body_types = params.getlist('body_types', None)
    unsafe_transmissions = params.getlist('transmissions', None)
    unsafe_fuel_types = params.getlist('fuel_types', None)
    unsafe_colors = params.getlist('colors', None)
    unsafe_interior_colors = params.getlist('interior_colors', None)

    # qs = Car.objects.all()

    # filter with city if exists
    if unsafe_city_id is not None:
        city = get_object_or_404(City, id=unsafe_city_id)
        qs = qs.filter(state=city.state)

    # filter with price if exists
    if unsafe_min_price is not None:
        if unsafe_max_price is not None:
            if unsafe_min_price < unsafe_max_price:
                min_price = unsafe_min_price
                max_price = unsafe_max_price
                qs = qs.filter(price__range=(min_price, max_price))
            else:
                raise BadRequest('Invalid price range')
        else:
            # max_price not provided: filter by min_price only
            min_price = unsafe_min_price
            qs = qs.filter(price__gte=min_price)
    else:
        # only max_price is provided: filter by it
        if unsafe_max_price is not None:
            max_price = unsafe_max_price
            qs = qs.filter(price__lte=max_price)

    # filter by year if exists
    if unsafe_min_year is not None:
        if unsafe_max_year is not None:
            if unsafe_min_year < unsafe_max_year:
                min_year = unsafe_min_year
                max_year = unsafe_max_year
                qs = qs.filter(year__range=(min_year, max_year))
            else:
                raise BadRequest('Invalid year range')
        else:
            # only min_year is provided: filter by it
            min_year = unsafe_min_year
            qs = qs.filter(year__gte=min_year)
    else:
        if unsafe_max_year is not None:
            # only max_year is provided: filter by it
            max_year = unsafe_max_year
            qs = qs.filter(year__lte=max_year)

    # filter by mileage if exists
    if unsafe_mileage is not None:
        if unsafe_mileage >= 0:
            mileage = unsafe_mileage
            qs = qs.filter(mileage__lte=mileage)
        else:
            raise BadRequest('Invalid mileage value')

    # filter by models
    if unsafe_models:
        safe_models = unsafe_models
        qs = qs.filter(model__id__in=safe_models)

    # filter by body_types
    if unsafe_body_types :
        safe_body_types = unsafe_body_types
        qs = qs.filter(body_type__in=safe_body_types)

    # filter by transmissions
    if unsafe_transmissions:
        safe_transmissions = unsafe_transmissions
        qs = qs.filter(transmission__in=safe_transmissions)

    # filter by fuel_types
    if unsafe_fuel_types:
        safe_fuel_types = unsafe_fuel_types
        qs = qs.filter(fuel_type__in=safe_fuel_types)
    
    # filter by colors
    if unsafe_colors:
        safe_colors = unsafe_colors
        qs = qs.filter(color__in=safe_colors)

    # filter by interior colors
    if unsafe_interior_colors:
        safe_interior_colors = unsafe_interior_colors
        qs = qs.filter(interior_color__in=safe_interior_colors)

    return qs
