from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):
    pass

class Category(models.Model):
    """
    Class to describe category
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("id",)


class Characteristic(models.Model):
    """
    Class to describe characteristic
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "characteristic"
        verbose_name_plural = "characteristics"
        ordering = ("id",)
        

class CategoryCharacteristic(models.Model):
    """
    Class to describe category characteristic
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_characteristics')
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, related_name='cat_characteristics')
    
    def __str__(self):
        return f'{self.category}: {self.characteristic}'

    class Meta:
        verbose_name = "category characteristic"
        verbose_name_plural = "category characteristics"
        ordering = ("id",)


class Advertisement(models.Model):
    """
    Class to describe advertisement
    """
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='advertisements')
    price = models.DecimalField(decimal_places=2, max_digits=16, validators=[MinValueValidator(0.00)])
    viewed_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "advertisement"
        verbose_name_plural = "advertisements"
        ordering = ("id",)


class Photo(models.Model):
    """
    Class to describe advertisement photo
    """
    photo = models.ImageField(upload_to='photo')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return f'фотография к объявлению {self.advertisement}'

    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photos"
        ordering = ("id",)


class AdvertisementCharacteristic(models.Model):
    """
    Class to describe advertisement characteristic
    """
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='adv_characteristics')
    characteristic = models.ForeignKey(Characteristic, on_delete=models.CASCADE, related_name='adv_characteristics')
    value = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.characteristic.name}: {self.value}'

    class Meta:
        verbose_name = "advertisement characteristic"
        verbose_name_plural = "advertisement characteristics"
        ordering = ("id",)
