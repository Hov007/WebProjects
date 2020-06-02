from django.contrib import admin

from .models import Menu, Order, OrderItem, Delivery, Size

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'name', 'size']
    class Meta:
        model = Menu

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'small', 'large']
    list_editable = ['small', 'large']
    class Meta:
        model = Size

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'complete']
    list_editable = ['complete']
    class Meta:
        model = Order

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'price', 'date_added']
    list_editable = ['quantity']
    class Meta:
        model = OrderItem

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'address', 'city', 'phonenumber', 'date_added']
    class Meta:
        model = Delivery

# Register your models here.
admin.site.register(Menu, MenuAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Size, SizeAdmin)