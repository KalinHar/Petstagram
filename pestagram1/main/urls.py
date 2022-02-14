from django.urls import path

from pestagram1.main.views.generic import show_home, show_dashboard
from pestagram1.main.views.pet_photos import show_pet_photo_details, create_pet_photo, edit_pet_photo, like_pet_photo
from pestagram1.main.views.pets import create_pet, edit_pet, delete_pet
from pestagram1.main.views.profiles import show_profile, create_profile, edit_profile, delete_profile

urlpatterns = (
    path('', show_home, name='index'),
    path('dashboard/', show_dashboard, name='dashboard'),

    path('profile/', show_profile, name='profile details'),
    path('profile/creare/', create_profile, name='crete profile'),
    path('profile/edit/', edit_profile, name='edit profile'),
    path('profile/delete/', delete_profile, name='delete profile'),

    path('pet/add/', create_pet, name='create pet'),
    path('pet/edit/<int:pk>/', edit_pet, name='edit pet'),
    path('pet/delete/<int:pk>/', delete_pet, name='delete pet'),

    path('photo/details/<int:pk>/', show_pet_photo_details, name='pet photo details'),
    path('photo/add/', create_pet_photo, name='create pet photo'),
    path('photo/edit/<int:pk>/', edit_pet_photo, name='edit pet_photo'),
    path('photo/like/<int:pk>/', like_pet_photo, name='like pet photo'),
)
