from django.shortcuts import render
from django.views import View
from .models import CategoryModel ,ProductModel,BlogModel,PurchaseInvoice
from accounts.models import *
from django.core.paginator import Paginator
from django.db.models import F
from .forms import ContactForm
from django.contrib.auth.models import User  
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
# Create your views here.



class IndexView(View):
    template_name = 'shop/index.html'

    def get(self, request):
        products = ProductModel.objects.filter(quantity_available__gt=0).order_by('-created_at')[:5]     
        categories = CategoryModel.objects.all()
    
        context = {
        'products': products, 
        'categories':categories, 
        }
        return render(request, self.template_name, context)


class ShopView(View):
    template_name = 'shop/shop.html'
    items_per_page = 10

    def get(self, request):
        products = ProductModel.objects.filter(quantity_available__gt=0).order_by('-created_at')  

        paginator = Paginator(products, self.items_per_page)
        page_number = request.GET.get('page')  
        page_products = paginator.get_page(page_number)
  
        context = {
        'page_products': page_products,
        }

        return render(request, self.template_name, context)



class ProductSingleView(View):
    template_name = 'shop/product-single.html'

    def get(self, request, pk):
        product = ProductModel.objects.get(id=pk)  
        related_products = ProductModel.objects.filter(category=product.category).order_by('-created_at').exclude(id=pk)[:5]
        
        context = {'product': product, 'related_products': related_products}
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        product = ProductModel.objects.get(id=pk)
        quantity = int(request.POST.get('quantity', 1)) 
        # ProductModel.objects.filter(id=pk).update(quantity_available=F('quantity_available') - quantity)
        # product.refresh_from_db()

        context = {'product': product}
        return render(request, self.template_name, context)



class ContactView(View):
    template_name = 'shop/contact.html'

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            
            if request.user.is_authenticated:
                contact.user = request.user
            else:
                contact.user = None  
            
            contact.save()
            # return render(request, 'shop/success.html')
            
        return render(request, self.template_name, {'form': form})




class BlogView(View):
    template_name = 'shop/blog.html'

    def get(self, request):
        blogs = BlogModel.objects.order_by('-created_at')
        products = ProductModel.objects.all()  
        context = {'blogs': blogs, 'products': products}

        return render(request, self.template_name, context)



class BlogSingleView(View):
    template_name = 'shop/blog-single.html'

    def get(self, request, pk):
        try:
            blog = BlogModel.objects.get(id=pk) 
            context = {'blog': blog}
            return render(request, self.template_name, context)
        except BlogModel.DoesNotExist:
            return HttpResponse("موردی یافت نشد")





class CartAddView(View):
    def post(self, request, product_id):
        try:
            product = ProductModel.objects.get(id=product_id)
            print(product,"ffffffeeeeeeeeeeeeeeeee")
        except ProductModel.DoesNotExist:
            return HttpResponseBadRequest("محصول مورد نظر وجود ندارد")

        if 'cart' not in request.session:
            print("no cart")
            request.session['cart'] = {}

        cart = request.session['cart']
        print("sssss",cart)

        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += 1
        else:
            cart[str(product.id)] = {
                'title': product.title,
                'price': product.price,
                'quantity': 1,
            }
        

        request.session['cart'] = cart
        request.session.modified = True
        
        return redirect('shop:cart_view')




class CartView(View):
    
    def get(self, request):
        print("qqqqqqqqqqqqqqqqqq")
        cart = request.session.get('cart', {})
        print(cart)
        if not cart:
            print("سبد خرید خالی است")
        
        total_price = 0
        total_quantity = 0 
        cart_items = []

        for product_id, item in cart.items():
            try:
                product = ProductModel.objects.get(id=product_id)
                item_total_price = product.price * item['quantity']
                total_price += item_total_price
                total_quantity += item['quantity']
                cart_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'item_total_price': item_total_price,
                })
            except ProductModel.DoesNotExist:
                print(f"محصول با شناسه {product_id} وجود ندارد")
        # total_quantity = sum(item['quantity'] for item in cart.values())

        print(total_quantity ,"jjjjj")
        return render(request, 'shop/cart.html', {'total_quantity': total_quantity,'cart':cart,'cart_items': cart_items, 'total_price': total_price})





class CartRemoveView(View):
    def post(self, request, product_id):
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            del cart[str(product_id)]

        request.session['cart'] = cart
        # updateCartQuantity()
        return redirect('shop:cart_view')










class PurchaseInvoiceView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        total_price = 0

        for product_id, item in cart.items():
            try:
                product = ProductModel.objects.get(id=product_id)
                
                total_price += product.price * item['quantity']
            except ProductModel.DoesNotExist:
                pass

        user = request.user
        purchase_invoice = PurchaseInvoice.objects.create(user=user, cost=total_price)

        addresses = UserAddressModel.objects.filter(user=user)
        # if not addresses.exists():
        #     return redirect('accounts:create_address')

        return render(request, 'shop/purchase_invoice.html', {'cart': cart, 'purchase_invoice': purchase_invoice, 'addresses': addresses})

    def post(self, request):
        selected_address_id = request.POST.get('selected_address')
        
        if selected_address_id is None:
            return HttpResponse('No address selected.')

        try:
            selected_address = UserAddressModel.objects.get(id=selected_address_id)
        except UserAddressModel.DoesNotExist:
            return HttpResponse('Selected address not found.')

        cart = request.session.get('cart', {})
        total_price = 0

        for product_id, item in cart.items():
            try:
                product = ProductModel.objects.get(id=product_id)
                total_price += product.price * item['quantity']
            except ProductModel.DoesNotExist:
                pass

        user = request.user
        purchase_invoice = PurchaseInvoice.objects.create(user=user, cost=total_price, address=selected_address)
        # request.session['cart'] = {}

        # return render(request, 'shop/purchase_invoice.html', {'purchase_invoice': purchase_invoice})
        return redirect('shop:shop')



class CheckoutView(View):
    template_name = 'shop/checkout.html'

    def get(self, request):
        # request.session['cart'] = {}
        return render(request, self.template_name)





# def is_admin(user):
#     return user.is_authenticated and (user.is_staff or user.is_superuser or user.is_admin)
#     # and user.username == 'علی'

class AdminPanelView(UserPassesTestMixin, View):
    template_name = 'shop/admin_panel.html'

    def test_func(self):
        # myapp.can_view_mymodel
        return self.request.user.has_perm('shop.can_view_products') and self.request.user.is_authenticated  
        # self.request.user.username == 'علی'

    def handle_no_permission(self):
        return redirect('shop:access_denied_page')


    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     if not self.request.user.has_perm('shop.view_products'):
    #         return redirect('shop:access_denied_page')
    #     return super().dispatch(*args, **kwargs)

    
    # def test_func(self):
    #     return is_admin(self.request.user)


    # def handle_no_permission(self):
    #     return redirect('shop:access_denied_page')


 


    def get(self, request):
        # if request.user.groups.filter(name='karmandan').exists():
        products = ProductModel.objects.all()
        total_stock = products.aggregate(Sum('quantity_available'))['quantity_available__sum']
        
        invoices = PurchaseInvoice.objects.all()
        total_revenue = invoices.aggregate(Sum('cost'))['cost__sum']

        context = {
            'products': products,
            'total_stock': total_stock or 0,
            'total_revenue': total_revenue or 0,
        }
        return render(request, self.template_name, context)

class AccessDeniedView(View):
    def get(self, request):
        return render(request, 'shop/access_denied.html')






class ProductDeliveryView(View):
    template_name = 'shop/delivery.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if self.request.user.has_perm('shop.view_purchaseinvoice'):
            invoices = PurchaseInvoice.objects.all()
            # filter(status='pending')

            products_to_deliver = []
            for invoice in invoices:
                user = invoice.user
                address = invoice.address
                products = invoice.products.all()
                products_count = len(products)
                products_to_deliver.append({
                    'user': user,
                    'address': address,
                    'products_count': products_count,
                    'products': products
                })

            context = {
                'products_to_deliver': products_to_deliver
            }

            return render(request, self.template_name, context)







class GetCartQuantityView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        total_quantity = sum(item['quantity'] for item in cart.values())
        
        return JsonResponse({'total_quantity': total_quantity})










class AboutView(View):
    template_name = 'shop/about.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)



class WishListView(View):
    template_name = 'shop/wishlist.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)