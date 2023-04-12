from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Все заказы"

    order_id = models.IntegerField(
        primary_key=True, verbose_name="Номер заказа", null=False
    )
    user_id = models.BigIntegerField(
        verbose_name="Телеграмм ID пользователя", null=False
    )
    item_id = models.IntegerField(verbose_name="ID товара", null=False)
    count = models.IntegerField(verbose_name="Количество", null=False)

    def __str__(self):
        return f"Заказ №{self.order_id} Пользователь: {self.user_id} Товар: {self.item_id} Количество: {self.count}"


class User(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    user_id = models.BigIntegerField(
        primary_key=True, verbose_name="Телеграмм ID пользователя", null=False
    )

    def __str__(self):
        return f"Пользователь: {self.user_id}"


class Item(models.Model):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    item_id = models.IntegerField(
        primary_key=True, verbose_name="ID товара", null=False
    )
    category = models.CharField(max_length=50, null=False)
    subcategory = models.CharField(max_length=50, null=False)
    photo_id = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"Заказ №{self.order_id} Пользователь: {self.user_id} Товар: {self.item_id} Количество: {self.count}"
