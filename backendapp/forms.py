from django import forms
from .models import Customer, Category, Brand, Product, Cart, CartProduct, Order, Review,Inquiry,Profile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    
# User Form
class UserRegistrationForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Customer
        fields = [ "username", "password", "email",]
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Customer with this username already exists.")
        return uname
    
    

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# Brand Form
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'brand', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# Cart Form
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['customer', 'total']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
        }


# Cart Product Form
class CartProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ['cart', 'product', 'rate', 'quantity', 'subtotal']
        widgets = {
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Subtotal'}),
        }


# Order Form
class CkeckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['cart', 'ordered_by', 'shipping_address', 'phone', 'email', 'subtotal', 'total', 'order_status']
        widgets = {
            'cart': forms.Select(attrs={'class': 'form-control'}),
            'ordered_by': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Subtotal'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total'}),
            'order_status': forms.Select(attrs={'class': 'form-control'}),
        }


# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }


#For CheckOut
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ordered_by","shipping_address", "phone","email"]
    

#For Customer Register
class CustomerRegistrationForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())
    email= forms.CharField(widget=forms.EmailInput())


    class Meta:
        model = Customer
        fields = [ "username", "password", "email"]
    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Customer with this username already exists.")
        return uname


#For Customer Login
class CustomerLoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())


#For InquiryForm
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']  # Customize fields as needed
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'message'}),
        }


#for Profile of Owner
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'dob','qualification','post']  # Customize fields as needed
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),            
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'date of birth'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'qualification'}),
            'post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'post of this website'}),

        }
