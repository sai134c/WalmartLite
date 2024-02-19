from django.contrib import admin
from .models import Category
from mptt.admin import DraggableMPTTAdmin
from .models import *

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent')
    list_display_links = ('indented_title',)
    ordering = ('tree_id', 'level', 'lft')

admin.site.register(Category, CategoryAdmin)


admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(ProductImage)
admin.site.register(Brand)
