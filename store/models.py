from django.db import models
from users.models import UserModel


class CategoryModel(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(unique=True, db_index=True, max_length=128)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категорию'


class ItemModel(models.Model):
    name = models.CharField(max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=128)
    category = models.ForeignKey(to=CategoryModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    tags = models.ManyToManyField(to='TagModel', blank=True, related_name='tags')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'вещи'
        verbose_name_plural = "вещи"


class BasketModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'корзину'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'{self.item}: {UserModel.objects.get(id=self.user.id).username}'


class TagModel(models.Model):
    tag = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, unique=True, db_index=True)

    def __str__(self):
        return 'Тег: ' + str(self.tag)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
