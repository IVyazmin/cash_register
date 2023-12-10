from django.contrib import admin

from register_app.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price"]
