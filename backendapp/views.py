from django.shortcuts import render,redirect,redirect, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView,ListView,DetailView,FormView,CreateView
from .forms import *
from .models import *
from django.http import Http404, JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.views import View


#For Mixin
class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('backendapp:user_login'))  # Redirects to login page if not authenticated
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
    

# User Signup View
class SignupView(CreateView):
    template_name ="admintemplates/user/signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("backendapp:dashboard")

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


# User Login View
class UserLoginView(TemplateView):
    template_name = "admintemplates/user/login.html"
    success_url = reverse_lazy('backendapp:dashboard')

    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        return render(request, self.template_name, {'loginform': login_form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            # Authenticate with username and password
            user = authenticate(request, username=username, password=password)
            print('kkkkkkkkkkk',user)
            print(password,username)
            if user:

                login(request, user)
                messages.success(request, "Login successful.")
                return redirect(self.success_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")

        return render(request, self.template_name, {'loginform': login_form})



# User Logout View
class UserLogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('backendapp:user_login')


#For Dashboard
class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "admintemplates/home.html"


#For Product List
class ProductListView(TemplateView):
    template_name = "admintemplates/product/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all product Brands
            product_list = Product.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(product_list, 5)  # Show 5 categories per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_categories = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_categories.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['product_list'] = paginated_categories  # Paginated category list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Product.DoesNotExist:
            context['product_list'] = None
            context['error'] = "No product list found."
            messages.error(self.request, "No brand found.")
        except Exception as e:
            context['product_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context
    

#For Product Create
class ProductCreateView(TemplateView):
    template_name = "admintemplates/product/create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        product_form = ProductForm(request.POST, request.FILES)
        
        try:
            if product_form.is_valid():
                product_form.save()
                messages.success(request, "product created successfully.")
                return redirect('backendapp:product_list')
            else:
                messages.error(request, "Sorry! The form is invalid.")
                return render(request, self.template_name, {'form': product_form})

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, self.template_name, {'form': product_form})
        

#For Product Update
class ProductUpdateView(TemplateView):
    template_name = "admintemplates/product/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('id')
        product = Product.objects.get(id=product_id)
        context['form'] = ProductForm(instance=product)

        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        product_obj = Product.objects.get(id=product_id)
        product_form = ProductForm(request.POST, request.FILES, instance=product_obj)
        if product_form.is_valid():
            product_form.save()
            return redirect('backendapp:product_list')
        else:
            return render(request, self.template_name, {'form': product_form, 'errors_message': 'sorry!!!Not valid'})


#For Product Delete
class ProductDeleteView(TemplateView):
    template_name = "admintemplates/product/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('id')

        try:
            context['product_delete'] = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404("product does not exist")
        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        try:
            product_delete = Product.objects.get(id=product_id)
            product_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("product does not exist")
        return redirect('backendapp:product_list')


#For Product Detail View
class ProductDetailView(TemplateView):
    template_name = "admintemplates/product/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('id')
        product_obj = get_object_or_404(Product, id=product_id)
        
        # Fetch comments and prepare the comment form
        comments = Review.objects.filter(product=product_obj)
        comment_form = ReviewForm()

        context.update({
            'product_detail': product_obj,
            'comments_list': comments,
            'comment_form': comment_form,
            'current_datetime': datetime.now()
        })

        return context

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        product_obj = get_object_or_404(Product, id=product_id)
        
        # Process the comment form
        comment_form = ReviewForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product_obj
            comment.author = request.user.username  # Assuming the user is logged in
            comment.save()

            return redirect('product_detail', id=product_id)  # Redirect to avoid duplicate submission

        # If form is invalid, return the context with form errors
        return self.render_to_response(self.get_context_data(comment_form=comment_form))
    

#For Brand
class BrandListView(TemplateView):
    template_name = "admintemplates/brand/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all product Brands
            brand_list = Brand.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(brand_list, 5)  # Show 5 categories per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_categories = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_categories.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['brand_list'] = paginated_categories  # Paginated category list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Brand.DoesNotExist:
            context['brand_list'] = None
            context['error'] = "No brand list found."
            messages.error(self.request, "No brand found.")
        except Exception as e:
            context['brand_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context
    

#For Brand Create
class BrandCreateView(TemplateView):
    template_name = "admintemplates/brand/create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BrandForm()
        return context

    def post(self, request, *args, **kwargs):
        brand_form = BrandForm(request.POST, request.FILES)
        
        try:
            if brand_form.is_valid():
                brand_form.save()
                messages.success(request, "brand is created successfully.")
                return redirect('backendapp:brand_list')
            else:
                messages.error(request, "Sorry! The form is invalid.")
                return render(request, self.template_name, {'form': brand_form})

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, self.template_name, {'form': brand_form})
        

#For Brand Update
class BrandUpdateView(TemplateView):
    template_name = "admintemplates/brand/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        brand_id = self.kwargs.get('id')
        brand = Brand.objects.get(id=brand_id)
        context['form'] = BrandForm(instance=brand)

        return context

    def post(self, request, *args, **kwargs):
        brand_id = self.kwargs.get('id')
        brand_obj = Brand.objects.get(id=brand_id)
        brand_form = BrandForm(request.POST, request.FILES, instance=brand_obj)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('backendapp:brand_list')
        else:
            return render(request, self.template_name, {'form': brand_form, 'errors_message': 'sorry!!!Not valid'})



#For Brand Delete
class BrandDeleteView(TemplateView):
    template_name = "admintemplates/brand/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        brand_id = self.kwargs.get('id')

        try:
            context['brand_delete'] = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise Http404("brand does not exist")
        return context

    def post(self, request, *args, **kwargs):
        brand_id = self.kwargs.get('id')
        try:
            brand_delete = Brand.objects.get(id=brand_id)
            brand_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("brand does not exist")
        return redirect('backendapp:brand_list')



#For Product Category
class CategoryCreateView(TemplateView):
    template_name = "admintemplates/category/create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        cat_form = CategoryForm(request.POST, request.FILES)
        
        try:
            if cat_form.is_valid():
                cat_form.save()
                messages.success(request, "category is created successfully.")
                return redirect('backendapp:cat_list')
            else:
                messages.error(request, "Sorry! The form is invalid.")
                return render(request, self.template_name, {'form': cat_form})

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, self.template_name, {'form': cat_form})
        

#For category of product
class CategoryListView(TemplateView):
    template_name = "admintemplates/category/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all product category
            category_list = Category.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(category_list, 5)  # Show 5 categories per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_categories = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_categories.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['category_list'] = paginated_categories  # Paginated category list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Brand.DoesNotExist:
            context['category_list'] = None
            context['error'] = "No category list found."
            messages.error(self.request, "No category found.")
        except Exception as e:
            context['category_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context
    

#For Category Update
class CategoryUpdateView(TemplateView):
    template_name = "admintemplates/category/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('id')
        category = Category.objects.get(id=cat_id)
        context['form'] = CategoryForm(instance=category)

        return context

    def post(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('id')
        cat_obj = Category.objects.get(id=cat_id)
        cat_form = CategoryForm(request.POST, request.FILES, instance=cat_obj)
        if cat_form.is_valid():
            cat_form.save()
            return redirect('backendapp:cat_list')
        else:
            return render(request, self.template_name, {'form': cat_form, 'errors_message': 'sorry!!!Not valid'})


#For Category Delete
class CategoryDeleteView(TemplateView):
    template_name = "admintemplates/category/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('id')

        try:
            context['cat_delete'] = Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            raise Http404("category does not exist")
        return context

    def post(self, request, *args, **kwargs):
        cat_id = self.kwargs.get('id')
        try:
            category_delete = Category.objects.get(id=cat_id)
            category_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("category does not exist")
        return redirect('backendapp:cat_list')


#For Order List
class OrderListView(TemplateView):
    template_name = "admintemplates/order/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch all product category
            order_list = Order.objects.all().order_by("-id")
            
            # Implement pagination
            paginator = Paginator(order_list, 8)  # Show 8 order per page
            page_number = self.request.GET.get('page')  # Get the page number from the request
            paginated_categories = paginator.get_page(page_number)  # Get paginated results
            total_pages = paginated_categories.paginator.num_pages  # Get total number of pages
            
            # Add data to the context
            context['order_list'] = paginated_categories  # Paginated category list
            context['lastpage'] = total_pages
            context['totalpagelist'] = [n + 1 for n in range(total_pages)]  # List of total pages

        except Order.DoesNotExist:
            context['order-list'] = None
            context['error'] = "No order list found."
            messages.error(self.request, "No order found.")
        except Exception as e:
            context['order_list'] = None
            context['error'] = f"An error occurred: {str(e)}"
            messages.error(self.request, f"An error occurred: {str(e)}")

        return context


#For Update
class OrderUpdateView(TemplateView):
    template_name = "admintemplates/order/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('id')
        order = Order.objects.get(id=order_id)
        context['form'] = CkeckOutForm(instance=order)

        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        order_obj = Order.objects.get(id=order_id)
        order_form = CkeckOutForm(request.POST, request.FILES, instance=order_obj)
        if order_form.is_valid():
            order_form.save()
            return redirect('backendapp:order_list')
        else:
            return render(request, self.template_name, {'form': order_form, 'errors_message': 'sorry!!!Not valid'})


#For Delete of Order
class OrderDeleteView(TemplateView):
    template_name = "admintemplates/order/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('id')

        try:
            context['order_delete'] = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404("order does not exist")
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        try:
            order_delete = Order.objects.get(id=order_id)
            order_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("order does not exist")
        return redirect('backendapp:order_list')


#Profile
class ProfileCreateView(TemplateView):
    template_name = "admintemplates/profile/create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        pro_form = ProfileForm(request.POST, request.FILES)
        
        try:
            if pro_form.is_valid():
                pro_form.save()
                messages.success(request, "profile is created successfully.")
                return redirect('backendapp:profile_list')
            else:
                messages.error(request, "Sorry! The form is invalid.")
                return render(request, self.template_name, {'form': pro_form})

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, self.template_name, {'form': pro_form})
        


#For ProfileList
class ProfileListView(TemplateView):
    template_name = 'admintemplates/profile/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_list'] = Profile.objects.all()
        return context
    

#For Profile Update
class ProfileUpdateView(TemplateView):
    template_name = "admintemplates/profile/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        pro_id = self.kwargs.get('id')
        profile = Profile.objects.get(id=pro_id)
        context['form'] = ProfileForm(instance=profile)

        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        pro_obj = Product.objects.get(id=order_id)
        order_form = ProfileForm(request.POST, request.FILES, instance=pro_obj)
        if order_form.is_valid():
            order_form.save()
            return redirect('backendapp:profile_list')
        else:
            return render(request, self.template_name, {'form': order_form, 'errors_message': 'sorry!!!Not valid'})


#For Profile Delete
class ProfileDeleteView(TemplateView):
    template_name = "admintemplates/profile/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('id')

        try:
            context['profile_delete'] = Profile.objects.get(id=order_id)
        except Profile.DoesNotExist:
            raise Http404("profile does not exist")
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        try:
            order_delete = Profile.objects.get(id=order_id)
            order_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("order does not exist")
        return redirect('backendapp:profile_list')
    

#For Inquiry
class InquiryListView(TemplateView):
    template_name = 'admintemplates/inquiry/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiry_list'] = Inquiry.objects.all()
        return context
    

#For Inquery Update
class InquiryUpdateView(TemplateView):
    template_name = "admintemplates/inquiry/create.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        pro_id = self.kwargs.get('id')
        profile = Profile.objects.get(id=pro_id)
        context['form'] = ProfileForm(instance=profile)

        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        pro_obj = Product.objects.get(id=order_id)
        order_form = ProfileForm(request.POST, request.FILES, instance=pro_obj)
        if order_form.is_valid():
            order_form.save()
            return redirect('backendapp:profile_list')
        else:
            return render(request, self.template_name, {'form': order_form, 'errors_message': 'sorry!!!Not valid'})


#For Inquery Delete
class InquiryDeleteView(TemplateView):
    template_name = "admintemplates/inquiry/delete.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        inq_id = self.kwargs.get('id')

        try:
            context['inquiry_delete'] = Inquiry.objects.get(id=inq_id)
        except Inquiry.DoesNotExist:
            raise Http404("inquiry does not exist")
        return context

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('id')
        try:
            inquiry_delete = Inquiry.objects.get(id=order_id)
            inquiry_delete.delete()
            # cat_delete.delete(hard=True) we can do it delete parmanent

        except Exception as e:
            print(e, '#############')
            raise Http404("order does not exist")
        return redirect('backendapp:inquiry_list')