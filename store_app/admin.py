from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(ProductVariation)
admin.site.register(Payment)
admin.site.register(Order)