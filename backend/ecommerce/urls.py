from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path("products/filter/", views.filter_products, name="filter_products"),
]
