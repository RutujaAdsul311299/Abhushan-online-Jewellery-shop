"""
URL configuration for jwelleryproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from jwelleryapp import views
from django.conf import settings
from django.conf.urls.static import static    # for images to be displayed in the website      

from django.contrib.auth.decorators import login_required               

urlpatterns = [
    path('admin/', admin.site.urls),    # admin url
    path('', views.product, name='home'),  # home page url
    path('register/',views.register),  # register url
    path('logout/',views.user_logout),  # logout url
    path('login/',views.user_login),    # login url
    path('add_to_cart',views.add_to_cart, name='add_to_cart'), # add to cart url
    path('remove_from_cart',views.remove_from_cart, name='remove_from_cart'),  # remove from cart url
    path('products/<id>',views.product_detail),  # product detail url
    path('cart/',views.user_cart), # user cart url
    path('search',views.search_product),  # search url
    path('placeorder',views.get_order),  # place order url
    path('order',views.order, name='place_order'),  # order url
    path('add_address',views.createAddress , name='add_address'), # add address url
    path('payment/<payment>', views.show_payment, name='payment'),  # payment url
    path('payment_callback', views.payment_callback),  # payment success url


]




if settings.DEBUG:    # if debug is true then only we can see the images
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
