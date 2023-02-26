from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Categories)
admin.site.register(Bidinglist)
admin.site.register(ArchiveProduct)