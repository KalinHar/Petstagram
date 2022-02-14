from django.shortcuts import render, redirect

from pestagram1.main.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from pestagram1.main.models import PetPhoto, Pet, Profile
from pestagram1.main.helpers import get_profile


def show_profile(request):
    profile = get_profile()

    # pet_photos = PetPhoto.objects.filter(tagged_pets__user_profile=profile).distinct()
    pets = list(Pet.objects.filter(user_profile=profile))
    pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()

    total_likes = sum(pp.likes for pp in pet_photos)
    total_pet_photos = len(pet_photos)

    context = {
        'profile': profile,
        'total_likes': total_likes,
        'total_images': total_pet_photos,
        'pets': pets,
    }
    return render(request, 'profile_details.html', context)


def profile_actions(request, form_class, success_url, instance, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = form_class(instance=instance)
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def create_profile(request):
    return profile_actions(request, CreateProfileForm, 'index', Profile(), 'profile_create.html')
    # if request.method == 'POST':
    #     form = CreateProfileForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('index')
    # else:
    #     form = CreateProfileForm()
    # context = {
    #     'form': form,
    # }
    # return render(request, 'profile_create.html', context)


def edit_profile(request):
    return profile_actions(request, EditProfileForm, 'profile details', get_profile(), 'profile_edit.html')
    # profile = get_profile()
    # if request.method == 'POST':
    #     form = EditProfileForm(request.POST, instance=profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile details')
    # else:
    #     form = EditProfileForm(instance=profile)
    # context = {
    #     'form': form,
    # }
    # return render(request, 'profile_edit.html', context)


def delete_profile(request):
    return profile_actions(request, DeleteProfileForm, 'index', get_profile(), 'profile_delete.html')
