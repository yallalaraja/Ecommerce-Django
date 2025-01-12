from django.contrib import admin,messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode
from . import models

admin.site.site_header = 'Storefront Admin'
admin.site.index_title = 'Admin'

# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    search_fields = ['title']

    @admin.display(ordering = 'products')
    def product_count(self,collection):
        url = reverse('admin:store_product_changelist') + \
        '?'+urlencode({'collection__id':str(collection.id)})
        return format_html('<a href={}>{}</a>',url,collection.product_count)
        # return format_html('<a href=" http://www.google.com "> {}</a>',collection.product_count)

    def get_queryset(self,request):
        return super().get_queryset(request).annotate(
            product_count = Count('products')
        )

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self,request,model_admin):
        return [
            ('<200','LOW')
        ]

    def queryset(self,request,queryset):
        if self.value () == '<100':
            return queryset.filter(inventory__lt = 100)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title','slug']
    search_fields = ['title']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug':['title']
    }
    list_display = ['title','unit_price','inventory_status','collection']
    list_editable = ['unit_price']
    list_per_page = 3
    list_filter = ['collection','last_update',InventoryFilter]
    actions = ['clearInventory']
    # inlines = [TagInline]

    class Media:
        css = {
            'all':['store/styles.css']
        }

    def collection_title(self,product):
        return product.collection.title

    @admin.action(description='Clear Inventoy')
    def clearInventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(request,
            f'{updated_count} products were updated successfully',
            messages.SUCCESS
        )

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 200:
            return 'LOW'
        return 'OK'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_select_related = ['user']
    list_editable = ['membership']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']

class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self,instance):
        if instance.image.name!='':
            return format_html(f'<img src="{instance.image.url}" class=thumbnail />')
        return ''

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]

# admin.site.register(models.Collection)
# admin.site.register(models.Product)
