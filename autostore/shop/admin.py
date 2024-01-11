from django.contrib import admin
from import_export import resources
from .models import Advertisement, Car, Comment, News, Sale
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from django.urls import reverse
from django.utils.html import format_html

# resources

class CarResource(resources.ModelResource):

    def get_export_headers(self):
        headers = super().get_export_headers()
        for i, h in enumerate(headers):
            if h == 'brand':
                headers[i] = "Company"
            if h == 'model':
                headers[i] = "Car Model"
        return headers

    class Meta:
        model = Car

    def dehydrate_price(self, car):
        formatted_price = f"{car.price:.2f}руб."
        return formatted_price
    


class NewsResource(resources.ModelResource):

    class Meta:
        model = News


class AdvertisementResource(resources.ModelResource):

    class Meta:
        model = Advertisement


class SaleResource(resources.ModelResource):

    class Meta:
        model = Sale


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment
# resources
# inlines
class SaleInline(admin.TabularInline):
    model = Sale
    extra = 1
    fields = ('buyer', 'sale_price')
    show_change_link = True

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('user', 'text')
    show_change_link = True
# inlines
# admin
class CarAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('brand', 'model', 'year', 'price', 'created_at', 'link_to_sales')
    list_filter = ('brand', 'year')
    search_fields = ('brand', 'model', 'year')
    short_description = 'Short description for CarAdmin'
    resource_class = CarResource
    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'year', 'price')
        }),
        ('Description', {
            'fields': ('description', 'image')
        }),
    )
    inlines = [SaleInline, CommentInline]

    def link_to_sales(self, obj):
        url = reverse('admin:shop_sale_changelist') + f'?car__id__exact={obj.id}'
        return format_html('<a href="{}">Sales</a>', url)

    link_to_sales.allow_tags = True
    link_to_sales.short_description = 'Sales for this Car'

    def get_export_queryset(self, request):
        return Car.objects.filter(price__gt=1)
    
    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLS,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


class NewsAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = NewsResource


class AdvertisementAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = AdvertisementResource


class SaleAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = SaleResource


class CommentAdmin(ExportMixin, SimpleHistoryAdmin):
    resource_class = CommentResource

# admin
# Register your models here.
admin.site.register(Car, CarAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Comment, CommentAdmin)
