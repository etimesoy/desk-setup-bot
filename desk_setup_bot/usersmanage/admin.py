from django.contrib import admin

from .models import User, Product, Discounts

# можно регистировать модели вот так
admin.site.register(Product)
admin.site.register(Discounts)


# а можно вот такю. Таким способом можно указать какие именно поля отображать в админке
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "referrer_id", "full_name", "username", "email")
