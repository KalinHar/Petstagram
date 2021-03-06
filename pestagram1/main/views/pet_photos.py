import os

from django.shortcuts import render, redirect

from pestagram1.main.forms import CreatePetPhotoForm
from pestagram1.main.models import PetPhoto


def show_pet_photo_details(request, pk):
    pet_photo = PetPhoto.objects \
        .prefetch_related('tagged_pets') \
        .get(pk=pk)

    context = {
        'pet_photo': pet_photo
    }
    return render(request, 'photo_details.html', context)


def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()

    return redirect('pet photo details', pk)


def pet_photo_actions(request, form_class, success_url, instance, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = form_class(instance=instance)
    context = {
        'form': form,
        'pet_photo': instance,
    }
    return render(request, template_name, context)


def create_pet_photo(request):
    return pet_photo_actions(request, CreatePetPhotoForm, 'dashboard', PetPhoto(), 'photo_create.html')


def edit_pet_photo(request, pk):
    return pet_photo_actions(request, CreatePetPhotoForm, 'dashboard', PetPhoto.objects.get(pk=pk), 'photo_edit.html')


def delete_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    image_path = pet_photo.photo.path
    pet_photo.delete()
    os.remove(image_path)

    return redirect('dashboard')

# Todo 401