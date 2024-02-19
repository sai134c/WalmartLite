from django.db import models
from mptt.models import TreeForeignKey, MPTTModel
from django.utils import timezone

class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name = 'Название')
    parent = TreeForeignKey('self', on_delete = models.PROTECT, null = True, blank = True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    slug = models.SlugField()

    discription = models.CharField(max_length=256, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.pk} {self.name}'
    
class Manufacturer(models.Model):
    name = models.CharField(verbose_name="Наименование Изготовителя", max_length=100)
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = 'Изготовитель'
        verbose_name_plural = 'Изготовители'

    def __str__(self) -> str:
        return self.name
    
class Brand(models.Model):
    name = models.CharField(verbose_name="Наименование бренда", max_length=100)
    description = models.TextField(verbose_name="Описание")
    categories = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField( max_length=50)
    discription = models.TextField(null=True,blank=True)
    creation_date = models.DateField(auto_now_add = timezone.now)

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0, max_digits=3, decimal_places=1, verbose_name='Скидка')

    #TODO - Decide
    #LINK - https://github.com/bmihelac/django-shop-discounts
    #LINK - https://docs.celeryq.dev/en/latest/userguide/tasks.html#task-options
    #LINK - https://forum.djangoproject.com/t/automatically-changing-the-value-of-a-model-field-upon-a-certain-time/11984/3
    #LINK - https://django-model-utils.readthedocs.io/en/latest/utilities.html#fieldtracker-implementation-details
    
    # start_disc 
    # end_disc
    has_discount = models.BooleanField(default=False)

    category = TreeForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name = 'Изготовитель')
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, verbose_name = 'Бренд', null=True)

    is_visible = models.BooleanField(default=True)
    images = models.ManyToManyField("ProductImage")

    # reviews = models.ManyToManyField("Review", verbose_name='Отзывы')
    # hit_count = 

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def calculate_price(self):
        if self.has_discount:
            return round(self.price-self.price*self.discount/100,2)
        return self.price
    
    def __str__(self) -> str:
        return f'{self.manufacturer.name} - {self.name} ${self.calculate_price()}'
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to=f'product_images')

from django.dispatch import receiver
import os


@receiver(models.signals.pre_delete, sender=Product)
def auto_delete_rel_on_obj_delete(sender, instance:Product, **kwargs):
    print(f'The Product \'{instance.name}\' is being deleted')
    for prodimage in instance.images.all():
        if hasattr(prodimage, 'image') and prodimage.image:
            image_path = prodimage.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
                print(f"\t----->File '{prodimage.image}' is deleted")
        prodimage.delete()