from django.urls import path
from .views import *
from .views import (
    IndexView,
    ShopView,
    ProductSingleView,
    ContactView,
    CheckoutView,
    CartView,
    CartAddView, 
    CartRemoveView,
    BlogView,
    BlogSingleView,
    AboutView,
    WishListView,
    PurchaseInvoiceView,
    # AdminDashboardView, 
    # AccessDeniedView
)
app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<int:pk>/', ProductSingleView.as_view(), name='product-single'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('cart/', CartView.as_view(), name='cart_view'),

    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<int:pk>/', BlogSingleView.as_view(), name='blog-single'),
    path('about/', AboutView.as_view(), name='about'),
    path('about/', WishListView.as_view(), name='about'),

    path('purchase-invoice/', PurchaseInvoiceView.as_view(), name='purchase_invoice'), 


    path('access-denied/', AccessDeniedView.as_view(), name='access_denied_page'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin_panel'),

    path('delivery/', ProductDeliveryView.as_view(), name='product_delivery'),

    path('get_cart_quantity/', GetCartQuantityView.as_view(), name='get_cart_quantity'),

]