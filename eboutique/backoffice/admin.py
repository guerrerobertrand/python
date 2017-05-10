from django.contrib import admin
from backoffice.models import *

# Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'code')

class ProductItemAdmin(admin.TabularInline):
    model = ProductItem
    raw_id_fields = ["attributes"]

# class ProductAdmin(admin.ModelAdmin):
#     model = Product
#     inlines = [ProductItemAdmin,]
#     list_display = ["id", "name", "price_ht", "price_ttc", "code"]
#     list_editable = ["name", "price_ht", "price_ttc"]

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'date_creation', 'status')
    search_fields = ('name', 'status')
    radio_fields = {"status": admin.VERTICAL}


class ProductFilter(admin.SimpleListFilter):

    title = 'filtre produit'
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin):
        return (
            ('online', 'En ligne'),
            ('offline', 'Hors ligne'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'online':
            return queryset.filter(status=1)

        if self.value() == 'offline':
            return queryset.filter(status=0)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem)