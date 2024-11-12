from django.urls import path
from .views import *

app_name = 'frontendapp'

urlpatterns = [
    # Home Page
    path('', HomeView.as_view(), name='home'),

    # Product Detail
    path('product/<int:id>/detail/', ProductDetailView.as_view(), name='product_details'),

    # Cart Management
    path('add-to-cart/<int:id>/', AddToCartView.as_view(), name='addtocart'),
    path('my-cart/', MyCartView.as_view(), name='myCart'),
    path('manage-cart/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
    path('manage-cart/', EmptyCartView.as_view(), name='emptycart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),

    # Customer Authentication
    path('signup/', CustomerRegisterView.as_view(), name='customer_registration'),
    path('logout/', CustomerLogoutView.as_view(), name='customerlogout'),
    path('login/', CustomerLoginView.as_view(), name='customerlogin'),

    # Customer Services
    path('customer-services/', CustomerServicesView.as_view(), name='customer_services'),

    # Review Management (Edit and Delete)
    path('review/<int:id>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('like-review/<int:review_id>/', like_review, name='like_review'),

    # Product Search
    path('search/', SearchView.as_view(), name='search_product'),

    # Product List
    path('product/list/', ProductListView.as_view(), name='product_list'),
]
