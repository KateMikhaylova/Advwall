from django.db import models


class Country(models.Model):
    """
    Class to describe country
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"
        ordering = ("id",)


class City(models.Model):
    """
    Class to describe city
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        ordering = ("id",)


class Street(models.Model):
    """
    Class to describe street
    """
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='streets')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "street"
        verbose_name_plural = "streets"
        ordering = ("id",)
