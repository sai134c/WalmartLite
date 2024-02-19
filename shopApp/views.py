from django.shortcuts import render
from .models import Brand, Product, Category

def home_page(request):
    return render(request, 'base.html', {})

def cat_list(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'shop/category_list.html', {'categories':categories})

def category(request,cid):
    categories = Category.objects.get(pk=cid).get_descendants(False)
    products = Product.objects.filter(is_visible = True, category__in=categories)
    
    context = {
        'cid':cid,
        'products':products,
        'categories':categories
    }
    return render(request, 'shop/category.html', context)

def sub_category(request,cid):
    brands = Brand.objects.filter(categories__id=cid)
    products = Product.objects.filter(is_visible = True, category_id=cid)
    context = {
        'brands':brands,
        'products':products
    }
    return render(request, 'shop/sub_category.html', context)

def brand_products(request, cid, bid):
    products = Product.objects.filter(is_visible = True, category_id=cid,  brand_id=bid)
    context = {
        'products':products
    }
    return render(request, 'shop/sub_category.html', context)

def product_detail(request, pid):
    product = Product.objects.get(pk=pid)
    context = {
        'product':product
    }
    return render(request, 'shop/product_detail.html',context)

def profile(request):
    return render(request, 'profile/profile.html', {})

def email_req(request):
    return render(request, 'profile/reg1.html', {})

