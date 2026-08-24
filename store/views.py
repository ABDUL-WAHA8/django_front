from django.shortcuts import get_object_or_404,render
from django.http import HttpRequest,HttpResponse
from django.db.models import Q,F,Func,Value
from django.db.models.functions import Concat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer ,ProductSerializer
from store.models import Product,Customer,Collection,OrderItem
from tags.models import Tag,TaggedItem



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

def get_customers_full_name(request):
    query_set=Customer.objects.annotate(
        full_name=Func(F('first_name'),Value(" "),F('last_name'),function='CONCAT')
    )
    return render(request,'query_set.html',{"customer_names":query_set})

def get_tag_products(request):
    taged_products=TaggedItem.active.CustomManager(Product,1)

    return render(request,'query_set.html',{"framework":"DJANGO !","tagged_products":list(taged_products)})

# Inserting data into the database using django orm
def inserting_data(request):
    # customer=Customer()
    # customer.birth_date="2000-4-28"
    # customer.email="corban22@gmail.com"
    # customer.first_name="Abdul"
    # customer.last_name="Wahab"
    # customer.membership="B"
    # customer.phone="03146765484"
    # customer.save()
    customer=Customer.objects.filter(first_name__icontains='Abdul')
    print(customer)

    return render(request,'query_set.html',{"framework":"DJANGO !"})

# Updating data in the database using django orm
def updating_data(request):
    # can be updated in two ways either by using the save method or by using the update method
    # save method

    # customer=Customer.objects.get(pk=1001)
    # customer.email="abbdul.wahab.dev@gmail.com"
    # customer.save()

    # update method

    # Customer.objects.filter(pk=1001).update(email="abbbdul.wahab.dev@gmail.com")

    # updated_customer=Customer.objects.get(pk=1001)


    delete_customer=Customer.objects.get(pk=1001)
    delete_customer.delete()
    # print(updated_customer)
    # Customer.objects.get(pk=1001)
    return render(request,"query_set.html",{"framework":"DJANGO!"})


@api_view(['Get'])
def customer_list(request):
    queryset=Customer.objects.all()
    serializer=CustomerSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['Get'])
def product_list(request):
    queryset=Product.objects.all()
    serializer=ProductSerializer(queryset,many=True)
    return Response(serializer.data)

@api_view(['Get'])
def product_individually(request,id):
    object=get_object_or_404(Product,id=id)
    serializer=ProductSerializer(object)
    return Response(serializer.data)