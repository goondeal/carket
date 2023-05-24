from modeltranslation.translator import translator, TranslationOptions
from .models import CarMakeCountry, CarMake, CarModel, CarBodyType, CarColor, CarDrivetrain, CarFeatureCategory, CarFeature, CarFuelType, CarTransmission, CarStatus, Car


class CarMakeCountryTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarMakeTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarModelTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarBodyTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarColorTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarDrivetrainTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarFeatureCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarFeatureTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarFuelTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarTransmissionTranslationOptions(TranslationOptions):
    fields = ('name',)


class VehicleHistoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarStatusTranslationOptions(TranslationOptions):
    fields = ('name',)


class CarTranslationOptions(TranslationOptions):
    fields = (
        'transmission',
        'body_type',
        'fuel_type',
        'color_name',
        'interior_color_name',
        'price_currency',
    )


translator.register(CarMakeCountry, CarMakeCountryTranslationOptions)
translator.register(CarMake, CarMakeTranslationOptions)
translator.register(CarModel, CarModelTranslationOptions)
translator.register(CarBodyType, CarBodyTypeTranslationOptions)
translator.register(CarColor, CarColorTranslationOptions)
translator.register(CarDrivetrain, CarDrivetrainTranslationOptions)
translator.register(CarFeatureCategory, CarFeatureCategoryTranslationOptions)
translator.register(CarFeature, CarFeatureTranslationOptions)
translator.register(CarFuelType, CarFuelTypeTranslationOptions)
translator.register(CarTransmission, CarTransmissionTranslationOptions)
translator.register(CarStatus, CarStatusTranslationOptions)
translator.register(Car, CarTranslationOptions)
