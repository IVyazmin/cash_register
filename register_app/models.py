from django.db import models


class Item(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID товара")
    title = models.CharField(verbose_name="Название", max_length=100)
    price = models.FloatField(verbose_name="Цена")
