from django.contrib.auth.models import AbstractUser
from django.db import models

# from django.core.exceptions import ValidationError
from address.models import City, Country, Street

USER_TYPE_CHOICES = (
    ("private entity", "private entity"),
    ("legal entity", "legal entity"),
)


class User(AbstractUser):
    """
    Class to describe user
    """

    username = models.CharField(max_length=150, unique=True)

    email = models.EmailField(
        unique=True,
        error_messages={"unique": "A user with that email already exists.", }
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        error_messages={"unique": "A user with that phone number already exists.", }
    )

    type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default="private entity")

    street = models.ForeignKey(
        Street,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super(User, self).save(*args, **kwargs)
    #
    # def clean(self):
    #     print('clean')
    #     cleaned_data = super().clean()
    #     print(cleaned_data)
    #     street = cleaned_data.get('street')
    #     city = cleaned_data.get('city')
    #     country = cleaned_data.get('country')
    #     if street and street.city != city:
    #         raise ValidationError("'city' field should correspond with streets city field")
    #     if city.country != country:
    #         raise ValidationError("'country' field should correspond with cities country field")
    #     return cleaned_data

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    def __str__(self):
        return f"{self.username} {self.email}"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("id",)
