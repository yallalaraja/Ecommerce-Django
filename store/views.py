from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend,FilterSet
from django.db.models import Count
from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import api_view,action
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.response import Response
from .models import Product,Collection,Review,Cart,CartItem,Customer,Order,ProductImage
from .filters import ProductFilter
from .pagination import ProductPagination
from .serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer,ProductImageSerializer
from .permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,ViewCustomerHistoryPermission

#Class Based Views 
# ---------------- class based api_views for product model ---------------- #

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','post','patch','delete','head','options']
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)  

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        (customer_id,created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response('ok')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created) = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        # If we are updating quantity then we use the AddcartItem serialzer
        if self.request.method == "POST":
            return AddCartItemSerializer 
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']
    permission_classes = [IsAdminOrReadOnly]

    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self,request,*args,**kwargs):
        if OrderItems.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'product is associated with orderitems'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        return super().destroy(self,request,*args,**kwargs)

    # def delete(self,request,pk):
    #     if product.orderitems.count() > 0:
    #         return Response({'error':'product is associated with orderitems'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, pk=None):
        # Retrieve the collection instance with products count annotation
        collection = get_object_or_404(
            Collection.objects.annotate(products_count=Count('products')), pk=pk
        )

        # Check if the collection is associated with any products
        if collection.products_count > 0:
            return Response(
                {'error': 'Collection is associated with one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        # Delete the collection
        return super().destroy(self,request,*args,**kwargs)

    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error':'collection is associated with one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id'

    def delete(self,request,pk):
        if product.orderitems.count() > 0:
            return Response({'error':'product is associated with orderitems'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionList(ListCreateAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count('products'))

    def get_serializer_class(self):
        return CollectionSerializer

    def get_serializer_context(self):
        return {'request':self.request}

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count('products'))

    def get_serializer_class(self):
        return CollectionSerializer

    def get_serializer_context(self):
        return {'request':self.request}

    def delete(self,request,pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'collection is associated with one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(APIView):
#     def get(self,request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset,many=True,context={'request': request})
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response('ok')

# class ProductDetail(APIView):
#     def get(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def put(self,request,id):
#         product = get_object_or_404(Product,pk=id)
#         serializer = ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

    # def delete(self,request,id):
    #     if product.orderitems.count() > 0:
    #         return Response({'error':'product is associated with orderitems'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
# ---------------- class based api_views for collection model ---------------- #


# class CollectionList(APIView):
#     def get(self,request):
#         queryset = Collection.objects.annotate(products_count=Count('products'))
#         serializer = CollectionSerializer(queryset,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(status=status.HTTP_201_CREATED)

# class CollectionDetail(APIView):
#     def get(self,request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
#         serializer = CollectionSerializer(collection,context={'request':request})
#         return Response(serializer.data)
#     def put(self,request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
#         serializer = CollectionSerializer(collection,data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
#     def delete(self,request,pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error':'collection is associated with one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# Create your function based views here.
# ---------------- api_views for product model ---------------- #
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset,many=True,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok')
    
@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    if request.method == 'GET':    
        serializer = ProductSerializer(product)
        # serializer.save()
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({'error':'product is associated with orderitems'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------- api_views for collection model ----------------- #
@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection,context={'request':request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error':'collection is associated with one or more products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

