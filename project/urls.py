"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from core.views import IndexView, SearchCarsListView, search_make_by_name, Wishlist, add_car_to_wishlist, remove_car_from_wishlist, PublishedCars, RequestedCars
from accounts.views import SignupView


urlpatterns = [
    # accounts
    path('signup/', SignupView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    # core
    path('', IndexView.as_view(), name='index'),
    path('search/<str:country_code>/', SearchCarsListView.as_view(), name='search'),
    path('search-make/', search_make_by_name, name='search_make'),

    # core - wishlist
    path('wishlist/', Wishlist.as_view(), name='get_wishlist'),
    path('wishlist/add/<int:car_id>/', add_car_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:car_id>/', remove_car_from_wishlist, name='remove_from_wishlist'),

    # core - published cars
    path('cars/published/', PublishedCars.as_view(), name='get_published_cars'),
    # core - requested cars
    path('cars/requested/', RequestedCars.as_view(), name='get_requested_cars'),

    # admin
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
