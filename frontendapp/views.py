from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView,View,CreateView,FormView
from backendapp.forms import *
from backendapp.models import *
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
# View for liking reviews
from django.views.decorators.http import require_POST
from django.http import JsonResponse

#For Mixin
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):

        cart_id = request.session.get("cart_id")

        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request,*args,**kwargs)


#For HomeView
class HomeView(TemplateView):
    template_name = 'clienttemplates/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filter products by category
        product_list2 = Product.objects.filter(category__name="Man and Women Fashion").order_by('-id')
        context['product_list2'] = product_list2
        context['product_chunk'] = [product_list2[i:i+3] for i in range(0, len(product_list2), 3)]


        product_list1 = Product.objects.filter(category__name="Beauty and Cosmatic").order_by('-id')
        context['product_list1'] = product_list1
        context['product_chunk1'] = [product_list1[i:i+3] for i in range(0, len(product_list1), 3)]


        product_list3 = Product.objects.filter(category__name="Jewellery Accessories").order_by('-id')
        context['product_list3'] = product_list3
        context['product_chunk2'] = [product_list3[j:j+3] for j in range(0, len(product_list3), 3)]

        product_list4 = Product.objects.filter(category__name="FootWare Collection").order_by('-id')
        context['product_list4'] =product_list3
        context['product_chunk4'] = [product_list4[i:i+3] for i in range(0, len(product_list4), 3)]
        
        # Get unique brands for Beauty and Cosmetic products
        context['categories'] = Category.objects.all()  # Fetch all categories
        context['brands'] = Brand.objects.all()  # Fetch all categories


        return context


#For product List
class ProductListView(TemplateView):
    template_name = 'clienttemplates/productlist.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-id')
        return context
    

#For Product Detail
class ProductDetailView(TemplateView):
    template_name = 'clienttemplates/productdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product = get_object_or_404(Product, id=product_id)
        
        # Get all reviews for the product
        reviews = product.reviews.all()
        
        # Calculate total likes and comments for the product
        total_likes = sum(review.likes for review in reviews)
        total_comments = reviews.count()

        context['product'] = product
        context['reviews'] = reviews
        context['review_form'] = ReviewForm()
        context['total_likes'] = total_likes
        context['total_comments'] = total_comments
        
        # Check if a reply form should be displayed
        context['reply_review_id'] = self.request.GET.get('reply')  # review ID to display reply form
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['id']
        product = get_object_or_404(Product, id=product_id)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.customer = request.user.customer
            review.save()
            return redirect('frontendapp:product_details', id=product_id)
        
        context = self.get_context_data(**kwargs)
        context['review_form'] = review_form
        return self.render_to_response(context)


@require_POST
def like_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.likes += 1
    review.save()
    return redirect('frontendapp:product_details', id=review.product.id)


#For Product Search View
class SearchView(TemplateView):
    template_name = 'clienttemplates/searchbar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', '')  # Get search query from input

        # Perform a case-insensitive search
        results = Product.objects.filter(name__icontains=query) if query else []

        # Find related products (e.g., in the same category as the first result)
        related_products = []
        if results:
            first_product = results.first()  # Get the first product from results
            related_products = Product.objects.filter(
                category=first_product.category
            ).exclude(id=first_product.id)

        # Add results and related products to the context
        context['query'] = query
        context['results'] = results
        context['related_products'] = related_products
        return context
    

# #For update Delete
class ReviewDeleteView(TemplateView):
    template_name = "clienttemplates/reviewdelete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_id = self.kwargs.get('id')

        try:
            context['review_delete'] = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise Http404("Review does not exist")
        return context

    def post(self, request, *args, **kwargs):
        review_id = self.kwargs.get('id')
        try:
            review_delete = Review.objects.get(id=review_id)
            product_id = review_delete.product.id  # Retrieve the product ID before deleting
            review_delete.delete()
        except Review.DoesNotExist:
            raise Http404("Review does not exist")
        # Redirect to the product details page with the product ID
        return redirect('frontendapp:product_details', id=product_id)



#For AddTOCard
class AddToCartView(TemplateView):
    template_name = "clienttemplates/addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product_obj = Product.objects.get(id=product_id)

        #check if cart exist
        cart_id = self.request.session.get('id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

            #item already exist in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity +=1
                cartproduct.subtotal += product_obj.price
                cart_obj.save()

            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj,rate=product_obj.price,quantity=1, subtotal=product_obj.price)
                cart_obj.total +=product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj,product=product_obj, rate=product_obj.price,quantity=1,subtotal=product_obj.price)
            cart_obj.save()

        return context
    

#For MyCart
class MyCartView(TemplateView):
    template_name = 'clienttemplates/mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id')
        cart = None

        # Check if cart_id exists in session and get the cart, if available
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()

        # Calculate total amount if cart is found
        total_amount = sum(cp.subtotal for cp in cart.cartproduct_set.all()) if cart else 0

        # Add cart and total_amount to the context
        context['cart'] = cart
        context['total_amount'] = total_amount
        return context


#For Manage Cart
class ManageCartView(View):
    def get(self,request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj= cp_obj.cart  

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()

        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()

            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass

        return redirect("frontendapp:myCart")


#For Empty Cart
class EmptyCartView(View):
    def get(self,request, *arg, **kwargs):
        cart_id = request.session.get("id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("frontendapp:myCart")


#For Customer CheckOut
class CheckoutView(CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("frontendapp:home")
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect('/login/?next=/checkout')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
            context['cart'] = cart_obj
            
        return context
    
    def form_valid(self, form):
        cart_id =self.request.session.get('id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal= cart_obj.total
            form.instance.discount =0
            form.instance.total = cart_obj.total
            form.instance.order_status ="Order Received"
            del self.request.session['id']
        
        else:
            return redirect('frontendapp:home')

        return super().form_valid(form)
    

#User Register direct login 
class CustomerRegisterView(CreateView):
    template_name ="clienttemplates/signup.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("frontendapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


#For Customer Logout
class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("frontendapp:home")


#For Customer Login
class CustomerLoginView(FormView):
    template_name ="clienttemplates/login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("frontendapp:home")
    # form_valid method is a type of post method and is available in CreateView FormView and updateview.
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self. success_url


#For Customer Services
class CustomerServicesView(TemplateView):
    template_name = 'clienttemplates/customerservice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InquiryForm()
        context['profiles'] = Profile.objects.all()  # Fetch all profiles to display
        return context

    def post(self, request, *args, **kwargs):
        form = InquiryForm(request.POST)

        try:
            if form.is_valid():
                print(form.is_valid())
                form.save()
                messages.success(request, "Your inquiry has been submitted successfully.")
                return redirect(reverse_lazy('customer_service'))
            else:
                messages.error(request, "Sorry! The form is invalid.")
                context = self.get_context_data()
                context['form'] = form  # Include the form with errors
                return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            context = self.get_context_data()
            context['form'] = form  # Include the form with errors
            return render(request, self.template_name, context)