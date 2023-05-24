
def get_car_image_upload_path(instance, filename):
    '''
    used in models.CARIMAGE.img field
    [filename]: final name to be saved
    '''
    return f'images/cars/{instance.car.slug}/{filename}'
