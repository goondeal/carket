import json
import random
from datetime import date
from django.core.management.base import BaseCommand
from core.models import *
from management.models import *
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Add test data to the db'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to <file>.json')

    def _get_rand_digit(self):
        return random.randint(0, 9)

    def _get_rand_num(self):
        return random.randint(1, 100) * random.randint(1, 100)

    def _create_phone_number(self, country):
        return country.dailing_code + ''.join([str(self._get_rand_digit()) for i in range(country.phone_max_length-len(country.dailing_code))])

    def _create_user(self, first_name, last_name, gender, city):
        email = f"{first_name}_{last_name}{self._get_rand_num()}@{random.choice(['gmail', 'hotmail', 'yahoo'])}.com"
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=self._create_phone_number(city.state.country),
            date_of_birth=date(random.randint(1980, 2005),
                               random.randint(1, 12), random.randint(1, 28)),
            city=city,
            gender=gender,
        )
        user.set_password(f"{first_name}#123")
        user.save()

    def _parse_year_or_none(self, year_str):
        try:
            return int(year_str)
        except ValueError:
            return None

    def handle(self, *args, **kwargs):
        fpath = kwargs['file_path']
        images_path = '~/projects/python/scraping/car_info/images'
        data = None
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        countries = data['countries']
        for country_name in countries:
            country = CarMakeCountry.objects.create(
                name=countries[country_name]['name'],
                name_ar=countries[country_name]['name_ar'],
                flag_img=f"{images_path}/{countries[country_name]['name']}.png"
            )
            makes = countries[country_name]['makes']
            for make_dict in makes:
                make = CarMake.objects.create(
                    name=make_dict['name'],
                    name_ar=make_dict['name_ar'],
                    country_of_origin=country,
                    year=self._parse_year_or_none(make_dict['year']),
                    logo=f"{images_path}/make_logos/{make_dict['name']}.jpg"
                )
                models = make_dict.get('models') or []
                for model_dict in models:
                    model = CarModel.objects.create(
                        name=model_dict['name'],
                        name_ar=model_dict['name_ar'],
                        make=make,
                    )

        # Add CarBodyTypes
        body_types = data['body_type']
        for body_type_dict in body_types:
            body_type = CarBodyType.objects.create(
                name=body_type_dict['name'],
                name_ar=body_type_dict['name_ar'],
            )

        # Add TransmissionTypes
        transmission_types = data['transmission']
        for transmission_dict in transmission_types:
            transmission = CarTransmission.objects.create(
                name=transmission_dict['name'],
                name_ar=transmission_dict['name_ar'],
            )

        # Add DrivetrainTypes
        drivetrain_types = data['drivetrain']
        for drivetrain_dict in drivetrain_types:
            drivetrain = CarDrivetrain.objects.create(
                name=drivetrain_dict['name'],
                name_ar=drivetrain_dict['name_ar'],
            )

        # Add FuelTypes
        fuel_types = data['fuel_type']
        for fuel_dict in fuel_types:
            fuel = CarFuelType.objects.create(
                name=fuel_dict['name'],
                name_ar=fuel_dict['name_ar'],
            )

        # Add Colors
        colors = data['colors']
        for color_dict in colors:
            color = CarColor.objects.create(
                name=color_dict['name'],
                name_ar=color_dict['name_ar'],
                hex_code='#' + color_dict['hex'],
            )

        # Add features
        features = data['features']
        k = 1
        for feature_name in features:
            feature_category = CarFeatureCategory.objects.create(
                name=features[feature_name]['name'],
                name_ar=features[feature_name]['name_ar'],
                order=k*20
            )
            k += 1
            features_list = features[feature_name].get('features') or []
            l = 1
            for feature_dict in features_list:
                feature = CarFeature.objects.create(
                    name=feature_dict['name'],
                    name_ar=feature_dict['name_ar'],
                    category=feature_category,
                    order=l*20
                )
                l += 1

        # Add Database Users [100 for each country]
        boys = ['ali', 'ahmad', 'omar', 'mostafa', 'sam',
                'turky', 'aziz', 'ghazi', 'mina', 'fahd']
        girls = ['noha', 'salma', 'noura', 'yomna', 'nada',
                 'aya', 'ward', 'boshra', 'hind', 'toqa']
        countries = Country.objects.all()
        for country in countries:
            states = State.objects.filter(country=country)
            for i in range(50):
                s = random.choice(states)
                cities = City.objects.filter(state=s)

                self._create_user(random.choice(
                    boys), last_name=random.choice(boys), gender='M', city=random.choice(cities))
                self._create_user(random.choice(
                    girls), last_name=random.choice(boys), gender='F', city=random.choice(cities))

        # Add car status data
        car_status = data['car_status']
        for status_dict in car_status:
            status = CarStatus.objects.create(
                name=status_dict['name'],
                name_ar=status_dict['name_ar'],
                is_available=status_dict['is_available']
            )

        # Add Cars data [1000 for each country]
        countries = Country.objects.all()
        cc_list = list(range(1000, 5100, 100))
        for country in countries:
            print('Adding cars of', country.name)
            for i in range(100):
                if i > 99 and i % 100 == 0:
                    print('progress =', i)
                cities = City.objects.filter(state__country=country)
                cities = [c for c in cities if c.users.count()]
                c = random.choice(cities)

                user = random.choice(CustomUser.objects.filter(city=c))
                phone2 = None
                if random.randint(0, 9) < 5:
                    tail = list(str(user.phone))[4:]
                    random.shuffle(tail)
                    phone2 = str(user.phone)[:4] + ''.join(tail)

                contact = Contact.objects.create(
                    user=user,
                    city=c,
                    street=random.choice(
                        ['4 flowers street', '4 شارع الزهور']),
                    phone1=user.phone,
                    phone2=phone2,
                    # lon = models.DecimalField(max_digits=9, decimal_places=6, null=True)
                    # lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
                )
                transmision = random.choice(CarTransmission.objects.all())
                body_type = random.choice(CarBodyType.objects.all())
                fuel_type = random.choice(CarFuelType.objects.all())
                color = random.choice(CarColor.objects.all())
                interior_color = random.choice(CarColor.objects.all())
                Car.objects.create(
                    user=contact.user,
                    contact=contact,
                    country=c.state.country.name,
                    state=c.state.name,

                    description='''احداث الخطّة الموسوعة بعض عل, يتعلّق الأثنان الأهداف أخر ما, عل تلك سياسة ديسمبر الضروري. بين أدنى عليها اكتوبر عن.
                     ٣٠ كما إنطلاق انتباه تكاليف, قد قام بقصف ممثّلة ألمانيا. كل الشهير الشرقي اليابان حتى, دول هو لغزو ليبين رجوعهم.
                     تُصب الأرض الخارجية إذ عدد, قام حادثة اليابان بريطانيا تم.
                     أي كما يونيو استدعى النزاع, بين لم كردة العالم للأراضي.
                     إذ هناك قبضتهم بتخصيص جعل, والتي أوروبا الشرقية أي كما.''',
                    status=random.choice(CarStatus.objects.all()),

                    year=random.randint(1980, 2023),
                    mileage=random.randint(0, 200_000),
                    engine_cc=random.choice(cc_list),
                    model=random.choice(CarModel.objects.all()),
                    transmission=transmision.name,
                    transmission_ar=transmision.name_ar,
                    body_type=body_type.name,
                    body_type_ar=body_type.name_ar,
                    fuel_type=fuel_type.name,
                    fuel_type_ar=fuel_type.name_ar,
                    color_name=color.name,
                    color_name_ar=color.name_ar,
                    color_hex=color.hex_code,
                    interior_color_name=interior_color.name,
                    interior_color_name_ar=interior_color.name_ar,
                    price=random.randint(100_000, 3_000_000),
                    price_currency=c.state.country.currency,
                    price_currency_ar=c.state.country.currency_ar,
                )
