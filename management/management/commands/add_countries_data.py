import json
from django.core.management.base import BaseCommand
from management.models import *


class Command(BaseCommand):
    help = 'Adds countries data to the db'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to <file>.json')

    def handle(self, *args, **kwargs):
        fpath = kwargs['file_path']
        data = None
        with open(file=fpath, mode='r', encoding='utf-8') as f:
            data = json.loads(f.read())

        countries_in_mvp = ['egypt', 'saudi_arabia',
                            'emarates', 'qatar', 'kuwait', 'bahrain']
        for country_name in countries_in_mvp:
            print('Adding', country_name, '...')
            country_json = data[country_name]
            country = Country.objects.create(
                code=country_json['code'],
                name=country_json['name'],
                name_ar=country_json['name_ar'],
                currency=country_json['currency'],
                currency_ar=country_json['currency_ar'],
                lang=country_json['lang'],
                dailing_code=country_json['dailing_code'],
                phone_max_length=country_json['phone_max_length']
            )

            states_json = country_json.get('states')
            if states_json:
                i = 1
                for state_json in states_json:
                    state = State.objects.create(
                        name=state_json['name'],
                        name_ar=state_json['name_ar'],
                        country=country,
                        order=i*20
                    )
                    i += 1

                    cities_json = state_json.get('cities')
                    if cities_json:
                        j = 1
                        for city_json in cities_json:
                            city = City.objects.create(
                                name=city_json['name'],
                                name_ar=city_json['name_ar'],
                                state=state,
                                order=j*20
                            )
                            j += 1
                    else:
                        city = City.objects.create(
                            name=state_json['name'],
                            name_ar=state_json['name_ar'],
                            state=state,
                            order=20,
                        )
