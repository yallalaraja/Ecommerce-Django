from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem
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
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self,cart_item:Cart):
        return cart_item.quantity*cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self,cart:Cart):
        return sum([item.quantity*item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

