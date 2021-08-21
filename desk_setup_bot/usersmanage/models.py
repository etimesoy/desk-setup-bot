from django.db import models


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользоатель"
        verbose_name_plural = "Пользователи"

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Телеграм ID пользователя")
    referrer_id = models.BigIntegerField(verbose_name="Телеграм ID пригласившего")
    full_name = models.CharField(max_length=255, verbose_name="Полное имя пользователя")
    username = models.CharField(max_length=255, verbose_name="Юзернейм пользователя", null=True)
    email = models.CharField(max_length=255, verbose_name="Адресс электронной почты пользователя", null=True)

    def __str__(self):
        return f"№{self.id} ({self.telegram_id} - {self.full_name})"


class Discounts(TimeBasedModel):
    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    id = models.AutoField(primary_key=True)
    # в видосе было telegram_id = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    telegram_id = models.ForeignKey('self', unique=True, on_delete=models.CASCADE)
    amount = models.BigIntegerField(verbose_name="Размер скидки")

    def __str__(self):
        return f"№{self.telegram_id} имеет скидку {self.amount}"


class Product(TimeBasedModel):
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название товара")
    photo_link = models.TextField(verbose_name="Ссылка на картинку товара")
    price = models.IntegerField(verbose_name="Цена товара")
    description = models.TextField(verbose_name="Описание товара", null=True)

    def __str__(self):
        return f"№{self.id}) {self.name} - {self.price}₽"
