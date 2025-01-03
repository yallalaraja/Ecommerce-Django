from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Min,Max,Sum,Count
from django.db.models import Q,F,Value,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db import transaction
from store.models import Product,Order,Customer,Collection,OrderItem
from tags.models import Tag,TaggedItem,TaggedItemManager
# from tags.models.TaggedItemManager import get_for_tags

# Create your views here.
def hello(request):
# ----------- Updating the data using ORM -----------

    # collection = Collection.objects.filter(pk=16).update(title='Luggage Items')
    # collection = Collection(pk=15)
    # collection.title = 'Sport items'
    # collection.feature_product = None
    # collection.save()

# ----------- insert the data using ORM -------------
    # collection = Collection()
    # collection.title = 'Video Games console'
    # product = Product.objects.get(pk=2)
    # collection.feature_product = product
    # collection.save()

    # collection = Collection.objects.create(title='a',feature_product_id=1)
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 4
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 3
    #     item.unit_price = 50
    #     item.quantity = 10
    #     item.save()

    return render(request,'hello.html')
    # tags = TaggedItem.objects.get_for_tags(Product,1)

    # return render(request,'hello.html',{'tags':tags})
    # query_set = Product.objects.all()
    # query_set = Product.objects.get(pk=0)
    # try:
    #     query_set = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    # query_set = Product.objects.filter(pk=0).exists()
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    # query_set = Product.objects.order_by('unit_price','-title').reverse()
    # single_prod = Product.objects.earliest('unit_price')
    # single_prod = Product.objects.latest('unit_price')
    # query_set = Product.objects.filter(Q(unit_price__gt=1120) | Q(inventory__gt=200))
    # query_set = Product.objects.order_by('unit_price','-title') # (-) -> desc
    # query_set = Product.objects.filter(unit_price__gt=100)
    #  ------- filter(Keyword = value) ----------- #
    # query_set = Product.objects.filter(title__contains='Bluetooth')
    # query_set = Product.objects.filter(title__startswith='S')
    # query_set = Product.objects.filter(title__endswith='r')
    # query_set = Product.objects.values_list('id','title','collection__title')
    # query_set = Product.objects.only('id','title','collection__title')
    # query_set = Product.objects.defer('description')
    # query_set = Product.objects.select_related('collection').all()[:5]
    # query_set = Product.objects.prefetch_related('promotions').all()
    # query_set = Order.objects.select_related('customer').order_by('-placed_at').all()
    # query_set = Order.objects.select_related('customer').prefetch_related('order_items').order_by('-placed_at').all()
    # result = Product.objects.aggregate(Count('id'))
    # result = Product.objects.aggregate(Sum('unit_price'),min_price=Min('unit_price'))
    # query_set = Product.objects.annotate(new_id=F('id')+1)
    # query_set = Customer.objects.annotate(full_name = Func('first_name',Value(' '),'last_name',function='CONCAT'))
    # query_set = Customer.objects.annotate(full_name = Concat('first_name',Value(' '),'last_name'))
    # result = Customer.objects.annotate(order_items = Count('orders'))

    # discount_price = ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField())
    # query_set = Product.objects.annotate(
    #     disc_price = discount_price
    # )
    # return render(request,'hello.html',{'name':'raja','single_product':single_prod})
    # return render(request,'hello.html',{'name':'raja','orders':query_set,'result':result})
    # return render(request,'hello.html',{'products':query_set,'order_count':result})

    # return render(request,'hello.html')