from django import template
from shopApp.models import Category

register = template.Library()

@register.filter
def category_filter(qs, cid):
    return qs.filter(category_id=cid)

@register.filter
def get_chiled_cats(obj):
    return Category.objects.filter(parent = obj)


@register.filter
@register.inclusion_tag('shop/tags/draw_subcategories.html')
def draw_subcategories(obj_id):
    sub_categories = Category.objects.filter(parent_id=obj_id)
    context = {
        'sub_categories':sub_categories
    }
    return context