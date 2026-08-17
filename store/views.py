from django.shortcuts import render
from django.http import HttpRequest
from django.db.models import Q,F
from store.models import Product,Customer,Collection,OrderItem,Order

# Create your views here.
def check_db_query(request):
    prod_query_set=Product.objects.all()
    for product in prod_query_set:
        print(product)
    return render(request, 'query_set.html')

# task 1
def get_com_accounts(request):
    customer_query_set=Customer.objects.filter(email__icontains=".com")
    return render(request,'query_set.html',{'customer_query_set':customer_query_set})

# task 2

def get_null_featured_product(request):
    null_featured_prod_set=Collection.objects.filter(featured_product__isnull=True)
    return render(request,"query_set.html",{"null_prod":null_featured_prod_set})

# task 3
def get_low_inventory(request):
    low_inventory=Product.objects.filter(inventory__gt=10)
    return render(request,"query_set.html",{"low_inventory":low_inventory})

# task 4
def get_argu_values(request):
    # Q - set query for or and other bitwise operator
        # argu_set=Product.objects.filter(Q(unit_price__gt=20) | Q(inventory__gt=10)) 
    # simple one for and like operators
    argu_set=Product.objects.filter(unit_price__gt=20,inventory__gt=10)
    return render(request,"query_set.html",{"q_set":argu_set})

#task 5 -- Sorting the products by unit price in descending order

def sortings(request):
    # title sorted in asc order
    # sort_title_asc=Product.objects.order_by('title')
    # title sorted in desc order
    # sort_price_dsc=Product.objects.order_by('-unit_price')
    #a bit complex query
    filtered_products=Product.objects.filter(Q(inventory__gt=50) | Q(unit_price__gt=50))
    sort_price_dsc=filtered_products.order_by('unit_price').reverse()
    return render(request,"query_set.html",{'sorted_title':sort_price_dsc})

# task 6 -- finding ordered products titles
def finding_ordered_products(request):
    product_ids=OrderItem.objects.values('product')
    actual_product=Product.objects.filter(id__in=product_ids).order_by('title')

    return render(request,"query_set.html",{"ordered_products":actual_product})

# task 7 last 5 order 

def orders_n_customers(request):
    orders=OrderItem.objects.select_related('order__customer','product').order_by('-order').distinct()[:5]
    return render(request,'query_set.html',{'orders':orders})

# task 8 lets try annotation and db functions like concat etc 

