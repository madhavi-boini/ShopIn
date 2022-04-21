from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.Home,name="Home"),
    path('clothes/', views.clothes,name="clothes"),
    path('clothes/men/', views.men),
    path('clothes/women/', views.women),
    path('clothes/kids/', views.kids),
    path('register/', views.customer),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='Logout'),
    path('jewellery/', views.jewellery),
    path('furniture/', views.furniture),
    path('yourorders/', views.yourorders),
    path('cart/', views.cart,name='cart'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
