from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views

# router = SimpleRouter()
# router.register('products',views.ProductViewSet)
# router.register('collections',views.CollectionViewSet)

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)

products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',views.CartItemViewSet,basename='cart-items-detail')

urlpatterns = router.urls + products_router.urls + carts_router.urls

# urlpatterns = [
#     path('products_vset',views.ProductViewSet),
#     path('products_cbv',views.ProductList.as_view()),
#     path('products_cbv/<int:pk>',views.ProductDetail.as_view()),
#     path('collections_cbv/',views.CollectionList.as_view()),
#     path('collections_cbv/<int:pk>',views.CollectionDetail.as_view(),name='collection-detail'),
#     path('products/',views.product_list),
#     path('products/<int:id>',views.product_detail),
#     path('collections/',views.collection_list),
#     path('collections/<int:pk>',views.collection_detail,name='collection-detail')
# ]