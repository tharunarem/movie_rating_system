from django.contrib import admin
from ratingapp.models import *
# Register your models here.
admin.site.register(Movie)
admin.site.register(Rating)

@admin.register(Dummy)
class Dummpyadmin(admin.ModelAdmin):
    list_display=('dummyname','age')
# admin.site.register(Dummy,Dummpyadmin)

