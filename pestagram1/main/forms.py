from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from pestagram1.main.helpers import BootstrapFormMixin, DisabledFieldsFormMixin, get_profile
from pestagram1.main.models import Profile, PetPhoto, Pet


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    # 'class': 'form-control',  # this is from BootstrapFormMixin for each field
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Url',
                }
            ),
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    # 'class': 'form-control',  # this is from BootstrapFormMixin for each field
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Url',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email',
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                }
            ),
            'birth_date': forms.DateInput(
                attrs={
                    'placeholder': '1920-01-01',
                }
            ),
        }


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        pets = list(self.instance.pet_set.all())
        PetPhoto.objects.filter(tagged_pets__in=pets).delete()
        self.instance.delete()

        return self.instance

    class Meta:
        model = Profile
        fields = ()


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Pet
        exclude = ('user_profile',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    # 'class': 'form-control',  # this is from BootstrapFormMixin for each field
                    'placeholder': 'Enter pet name',
                }
            ),
        }


class EditPetForm(BootstrapFormMixin, forms.ModelForm):
    MIN_DATE = date(1920, 1,1)
    MAX_DATE = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean_birth_date(self):  # same validation as model Profile birth_date validation, but this in form
        birth_date = self.cleaned_data['birth_date']
        if birth_date < self.MIN_DATE or self.MAX_DATE < birth_date:
            raise ValidationError(f'Date must be between {self.MIN_DATE} and {self.MAX_DATE}')
        return birth_date

    class Meta:
        model = Pet
        exclude = ('user_profile',)
        widgets = {
            'name': forms.TextInput(
                attrs={
                    # 'class': 'form-control',  # this is from BootstrapFormMixin for each field
                    'placeholder': 'Enter pet name',
                }
            ),
        }


class DeletePetForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    # disabled_fields = 'name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Pet
        exclude = ('user_profile',)


def take_query():
    val = [(choice.name, choice) for choice in
           Pet.objects.filter(user_profile=get_profile())]
    return val


class CreatePetPhotoForm(forms.ModelForm):

    class Meta:
        model = PetPhoto
        fields = ('photo', 'description', 'tagged_pets')
        widgets = {
            'photo': forms.FileInput(
                attrs={
                    "class": "form-control-file",
                    "type": "file",
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter Description',
                    'rows': 3,
                }
            ),
            'tagged_pets': forms.SelectMultiple(
                # choices= Pet.objects.filter(user_profile=get_profile()).values('name'),
                choices=take_query(),

                attrs={
                    'class': 'form-control',
                }
            )
        }
        labels = {
            "tagged_pets": "Tag Pets",
            "photo": "Pet Image"
        }



#
# class CreatePetPhotoForm(forms.ModelForm):
#     tagged_pets = forms.MultipleChoiceField(choices=take_query())
#
#     class Meta:
#         model = PetPhoto
#         fields = ["photo", "description", "tagged_pets"]
#         widgets = {
#             "photo": forms.FileInput(attrs={
#                 "type": "file", "id": "file-upload", "name": "filename", "class": "form-control-file"
#             }),
#             "description": forms.Textarea(attrs={
#                 "type": "text", "id": "first_name", "name": "first_name", "placeholder": "Enter Description",
#                 "rows": 3, "class": "form-control"
#             }),
#             "tagged_pets": forms.SelectMultiple(
#             )
#         }
#
#         labels = {
#             "description": "Description",
#             "photo": "Pet Image"
#         }