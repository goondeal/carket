from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Car, CarMake, CarModel
from .services import get_filtered_cars
from management.models import Country


# Create your views here.
class IndexView(TemplateView):
    template_name = 'core/index.html'


class SearchCarsListView(ListView):
    paginate_by = 30
    model = Car
    template_name = 'core/search.html'

    def get_queryset(self):
        unsafe_country_code = self.kwargs.get('country_code', '')
        country = get_object_or_404(Country, code=unsafe_country_code)
        
        params = self.request.GET

        unsafe_page = params.get('page', 1)

        qs = super().get_queryset()
        qs = qs.filter(country=country, status__is_available=True)

        return get_filtered_cars(qs, params)


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["top_20_makes"] = CarMake.objects.all()[:20]
        return context


# class CarMakes()
def search_make_by_name(request):
    search_term = request.POST.get('make_search', None)
    if search_term:
        result = CarMake.objects.filter(name__istartswith=search_term)
        if result.count() > 0:
            html = '\n'.join([
                f''' <option value="{make}">{make}</option> ''' for make in result
            ])
            return HttpResponse(html)
    return HttpResponse('<p> No results found </p>')


class Wishlist(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Car
    template_name = 'core/wishlist.html'

    def get_queryset(self):
        user = self.request.user
        
        # unsafe_page = params.get('page', 1)

        # qs = super().get_queryset()
        qs = user.saved_cars.select_related('status').all()

        return qs



@login_required
def add_car_to_wishlist(request, car_id):
    user = request.user
    car = get_object_or_404(Car, id=car_id)
    if not user.saved_cars.filter(id=car_id).exists():
        user.saved_cars.add(car)
        return HttpResponse('Added Successfuly', status_code=200)
    return HttpResponse('Car already exists', status_code=400)


@login_required
def remove_car_from_wishlist(request, car_id):
    user = request.user
    car = get_object_or_404(Car, id=car_id)
    if user.saved_cars.filter(id=car_id).exists():
        user.saved_cars.remove(car)
        return HttpResponse('Removed Successfuly', status_code=200)
    return HttpResponse('Car already does not exists', status_code=400)


class PublishedCars(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Car
    template_name = 'core/user_published_cars.html'

    def get_queryset(self):
        user = self.request.user
        qs = user.own_cars.select_related('status').all()
        return qs


class RequestedCars(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Car
    template_name = 'core/user_requested_cars.html'

    def get_queryset(self):
        user = self.request.user
        qs = user.cars_list.select_related('status').all()
        return qs
