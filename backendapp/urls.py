from django.urls import path,include
from .views import *
from . import views  # Import views from the current directory


app_name = 'backendapp'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    #For Product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:id>update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:id>delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:id>detail/', ProductDetailView.as_view(), name='product_detail'),


    #For Brand
    path('brand/list/', BrandListView.as_view(), name='brand_list'),
    path('brand/create/', BrandCreateView.as_view(), name='brand_create'),
    path('brand/<int:id>update/', BrandUpdateView.as_view(), name='brand_update'),
    path('brand/<int:id>delete/', BrandDeleteView.as_view(), name='brand_delete'),


    #For Category Product
    path('cat/list/', CategoryListView.as_view(), name='cat_list'),
    path('cat/create/', CategoryCreateView.as_view(), name='cat_create'),
    path('cat/<int:id>update/', CategoryUpdateView.as_view(), name='cat_update'),
    path('cat/<int:id>delete/', CategoryDeleteView.as_view(), name='cat_delete'),


    #For Order
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/<int:id>update/', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:id>delete/', OrderDeleteView.as_view(), name='order_delete'),


    #For User Authentication
    path('signup/', SignupView.as_view(), name='signup'),  # Link the CBV signup view
    path('logout/', UserLogoutView.as_view(), name='user_logout'),  # Update the URL to use CBV
    path('login/', UserLoginView.as_view(), name='user_login'),  # Update the URL to use CBV


    #Profile
    path('profile/create', ProfileCreateView.as_view(), name='profile_create'), 
    path('profile/list', ProfileListView.as_view(), name='profile_list'), 
    path('profile/<int:id>/update/', ProfileUpdateView.as_view(), name='profile_update'), 
    path('profile/<int:id>/delete/', ProfileDeleteView.as_view(), name='profile_delete'), 


    #Inquiry
    path('inquiry/list', InquiryListView.as_view(), name='inquiry_list'), 
    path('inquiry/<int:id>/update/', InquiryUpdateView.as_view(), name='inquiry_update'), 
    path('inquiry/<int:id>/delete/', InquiryDeleteView.as_view(), name='inquiry_delete'), 



]