from django.contrib import admin

from .models import Car, Day, Ride, Review

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display = ['direction']

    class Meta:
        model = Car

class DayAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'hour', 'sits']
    list_editable = ['sits']

    class Meta:
        model = Day

class RideAdmin(admin.ModelAdmin):
    list_display = ['day', 'phonenumber', 'ticket']

    class Meta:
        model = Ride

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phonenumber', 'subject', 'text']

    class Meta:
        model = Review

admin.site.register(Car, CarAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Ride, RideAdmin)
admin.site.register(Review, ReviewAdmin)