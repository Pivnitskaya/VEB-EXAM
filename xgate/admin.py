from django.contrib import admin
from .models import ProductCategory, Product, Order, OrderItem, Promotion, SupportRequest


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ('name', 'price', 'is_active', 'system')
    readonly_fields = ()
    show_change_link = True


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    inlines = [ProductInline]
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_name', 'price', 'is_active', 'system')
    list_filter = ('category', 'is_active', 'system')
    search_fields = ('name', 'description', 'compatibility')
    list_display_links = ('name',)
    raw_id_fields = ('category',)

    @admin.display(description='Категория')
    def category_name(self, obj):
        return obj.category.name


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ('product',)
    readonly_fields = ()
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'email', 'created_at', 'total_items')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'phone', 'email')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)
    list_display_links = ('id', 'customer_name')

    @admin.display(description='Количество товаров')
    def total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name', 'quantity')
    raw_id_fields = ('order', 'product')
    search_fields = ('product__name',)

    @admin.display(description='Заказ ID')
    def order_id(self, obj):
        return obj.order.id

    @admin.display(description='Товар')
    def product_name(self, obj):
        return obj.product.name


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    list_display_links = ('title',)


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'support_type', 'submitted_at')
    list_filter = ('support_type', 'submitted_at')
    search_fields = ('name', 'phone', 'email', 'message')
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)
    list_display_links = ('name',)
