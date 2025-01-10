from rest_framework import serializers
from django.db import transaction
from .models import Product,Collection,Review,Cart,CartItem,Customer,Order,OrderItem
from decimal import Decimal

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date'] 

    def create(self,validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

    

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','slug','description','unit_price','inventory','price_with_tax','collection']
    price_with_tax = serializers.SerializerMethodField(method_name='calc_tax_method')
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name='collection-detail')
    # collection = serializers.StringRelatedField()
    # collection = serializers.PrimaryKeyRelatedField \
    # (queryset = Collection.objects.all())

    def calc_tax_method(self,product:Product):
        return product.unit_price * Decimal(1.1)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
# We are just updating the quantity we dont need to fetch all the details so making our product as read_only
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self,cart_item:Cart):
        return cart_item.quantity*cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product exists with given id')
        return value 
        
    def save(self,**kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self,cart:Cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date','membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','payment_status','items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    with transaction.atomic():
        def save(self,**kwargs):
            cart_id = self.validated_data['cart_id']
            (customer,created) = Customer.objects.get_or_create(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                )for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            return order
