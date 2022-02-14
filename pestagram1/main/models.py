from datetime import date, datetime

from django.core.validators import MinLengthValidator
from django.db import models

from pestagram1.main.validators import only_letters, file_max_size, correct_date, MinDateValidator


class Profile(models.Model):
    F_NAME_MAX = 30
    F_NAME_MIN = 2
    L_NAME_MAX = 30
    L_NAME_MIN = 2
    MIN_DATE = date(1920, 1, 1)

    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'
    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    first_name = models.CharField(
        max_length=F_NAME_MAX,
        validators=(
            MinLengthValidator(F_NAME_MIN),
            only_letters,
        ),
    )

    last_name = models.CharField(
        max_length=L_NAME_MAX,
        validators=(
            MinLengthValidator(L_NAME_MIN),
            only_letters,
        ),
    )

    picture = models.URLField()

    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=(
            # MinDateValidator(MIN_DATE),
            correct_date,
        ),

    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=True,
        blank=True,
    )


class Pet(models.Model):
    NAME_MAX = 30

    CAT = 'Cat'
    DOG = 'Dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH = 'Fish'
    OTHER = 'Other'
    TYPES = [(x, x) for x in (CAT, DOG, BUNNY, PARROT, FISH, OTHER)]

    name = models.CharField(
        max_length=NAME_MAX,
    )

    type = models.CharField(
        max_length=max(len(x) for x, _ in TYPES),
        choices=TYPES,
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    @property
    def age(self):
        return datetime.now().year - self.birth_date.year

    class Meta:
        unique_together = ('user_profile', 'name')


class PetPhoto(models.Model):
    photo = models.ImageField(
        validators=(
            file_max_size,
        )
    )

    tagged_pets = models.ManyToManyField(
        Pet,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.IntegerField(
        default=0,
    )

