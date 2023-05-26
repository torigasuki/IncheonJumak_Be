from django.contrib import admin

from review.models import Alcohol_Review, Brewery_Review,Event_Review

# Register your models here.
admin.site.register(Alcohol_Review)
admin.site.register(Brewery_Review)
admin.site.register(Event_Review)