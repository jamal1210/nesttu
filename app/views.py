from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.views import View
from.models import Customer, Product, Cart, OrderPlaced
from.forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#product views section 
class ProductViews(View):
    def get(self, request):
        Mens = Product.objects.filter(category='M')
        TShirt = Product.objects.filter(category='TS')
        KidsWear = Product.objects.filter(category='KD')
        Ladies = Product.objects.filter(category='L')
        FemaleDress = Product.objects.filter(category='EL')
        return render(request, 'app/index.html', {'Mens': Mens, 'TShirt': TShirt,'KidsWear':KidsWear,'Ladies':Ladies,'FemaleDress':FemaleDress})
    
    

class ProductDetailView(View):
    def get(self, request, pk):
        # Fetch the product using the primary key
        product = Product.objects.get(pk=pk)  # Corrected: Product with a capital P
        return render(request, 'app/productdetail.html', {'product': product})
    
    
# cart sections 
@login_required
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod-id')

        # Validate product ID
        if not product_id:
            return render(request, 'app/addtocart.html', {'error': "Invalid product ID."})

        # Fetch the product
        product = get_object_or_404(Product, id=product_id)

        # Add product to the cart
        Cart.objects.create(user=user, product=product)

        # Redirect to cart or success page
        return redirect('/cart')  # Replace 'cart' with your cart URL name

    return redirect('/cart')  # Redirect GET requests to product listing


def cart(request):
    user = request.user
    # Fetch the user's cart items
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'app/addtocart.html', {'cart_items': cart_items})



# checkout
@login_required
def check_out(request):
    user = request.user
    add = Customer.objects.filter(user=user)  # Get the customer's address
    cart_items = Cart.objects.filter(user=user)  # Get cart items for the user

    amount = 0.0
    shipping_amount = 120.0  # Fixed shipping cost
    total_amount = 0.0

    # Calculate the total amount for cart items
    for item in cart_items:
        amount += item.quantity * item.product.discounted_price

    total_amount = amount + shipping_amount if cart_items.exists() else 0.0

    # Render the template with the necessary context
    return render(request, 'app/checkout.html', {
        'add': add,
        'cart_items': cart_items,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount
    })


# cart display 
def cart_show(request):
    if request.user.is_authenticated:  # Check if the user is authenticated
        user = request.user
        cart_items = Cart.objects.filter(user=user)  # Fetch cart items for the user
        amount = 0.0
        shipping_amount = 120.0  # Fixed shipping cost
        total_amount = 0.0

        # Calculate total amount for cart items
        if cart_items.exists():  # Check if cart_items is not empty
            for cart_item in cart_items:
                temp_amount = cart_item.quantity * cart_item.product.discounted_price
                amount += temp_amount

            total_amount = amount + shipping_amount

        # Render the template and pass the required context
        return render(request, 'app/addtocart.html', {
            'cart_items': cart_items,
            'total_amount': total_amount,
            'amount': amount,
            'shipping_amount': shipping_amount
        })
    else:
        # Redirect to login if the user is not authenticated
        return redirect('login')



# PRODUCT ADD 
def pluscart(request):
    if request.method == 'GET':  # Ensure the method is 'GET'
        prod_id = request.GET.get('prod_id')  # Get the product ID from the request
        try:
            # Fetch the cart item for the current user and specified product
            c = Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
            c.quantity += 1  # Increment the quantity
            c.save()  # Save the changes to the database

            # Calculate amounts
            amount = 0.0
            shipping_amount = 120.0  # Fixed shipping cost
            cart_items = Cart.objects.filter(user=request.user)  # All cart items for the user

            for item in cart_items:
                amount += item.quantity * item.product.discounted_price

            total_amount = amount + shipping_amount

            # Prepare the response data
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount,
                'message': 'Cart updated successfully'
            }

            return JsonResponse(data)  # Return the data as a JSON response

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)  # Handle if cart item doesn't exist

    return JsonResponse({'error': 'Invalid request'}, status=400)  # Handle invalid request methods


#MINUS CART 
def minuscart(request):
    if request.method == 'GET':  # Ensure the method is 'GET'
        prod_id = request.GET.get('prod_id')  # Get the product ID from the request
        try:
            # Fetch the cart item for the current user and specified product
            c = Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
            c.quantity -= 1  # Increment the quantity
            c.save()  # Save the changes to the database

            # Calculate amounts
            amount = 0.0
            shipping_amount = 120.0  # Fixed shipping cost
            cart_items = Cart.objects.filter(user=request.user)  # All cart items for the user

            for item in cart_items:
                amount += item.quantity * item.product.discounted_price

            total_amount = amount + shipping_amount

            # Prepare the response data
            data = {
                'quantity': c.quantity,
                'amount': amount,
                'total_amount': total_amount,
                'message': 'Cart updated successfully'
            }

            return JsonResponse(data)  # Return the data as a JSON response

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)  # Handle if cart item doesn't exist

    return JsonResponse({'error': 'Invalid request'}, status=400)  # Handle invalid request methods



#remove cart  
def remove_cart(request):
    if request.method == 'GET':  # Ensure the request method is GET
        prod_id = request.GET.get('prod_id')  # Get the product ID from the request
        if not prod_id:
            return JsonResponse({'error': 'Product ID not provided'}, status=400)

        try:
            # Fetch the cart item for the current user and specified product
            cart_item = Cart.objects.get(Q(product__id=prod_id) & Q(user=request.user))
            cart_item.delete()  # Remove the item from the cart

            # Recalculate the total amounts
            amount = 0.0
            shipping_amount = 120.0  # Fixed shipping cost
            cart_items = Cart.objects.filter(user=request.user)  # Fetch remaining cart items

            for item in cart_items:
                amount += item.quantity * item.product.discounted_price

            total_amount = amount + shipping_amount if cart_items.exists() else 0.0

            # Prepare and send the JSON response
            return JsonResponse({
                'amount': amount,
                'total_amount': total_amount,
                'message': 'Cart updated successfully'
            })

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)

    # If the request method is not GET, return an error response
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def payment_done(request):
    custid = request.GET.get('custid')
    if not custid:
        return HttpResponse("confirm address")
    
    try:
        customer = Customer.objects.get(id=custid)
    except Customer.DoesNotExist:
        raise Http404("login first ")
    
    cart_items = Cart.objects.filter(user=customer.user)
    for item in cart_items:
        OrderPlaced.objects.create(
            user=item.user,
            customer=customer,
            product=item.product,
            quantity=item.quantity
        )
        item.delete()

    return redirect('orders')


def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})



#payment_form

from .forms import PaymentForm

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url_name')  # লেনদেন সফল হলে এই URL-এ রিডাইরেক্ট করুন
    else:
        form = PaymentForm()
    
    return render(request, 'app/payment_form.html', {'form': form})


def success_view(request):
    return render(request, 'app/succes_payment.html')



#optional
def buy_now(request):
 return render(request, 'app/buynow.html')





# personal information 

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # Get the current logged-in user
            user = request.user
            
            # Save the form data while associating it with the user
            customer_profile = form.save(commit=False)
            customer_profile.user = user
            customer_profile.save()

            # Add a success message
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to profile page
        else:
            # Re-render the form with error messages
            return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})
        




def address(request):
 add = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html',{'add':add,'active': 'btn-primary'})



#registration and login section 

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered successfully.')
            form.save()
            return redirect('login')  # Redirect to login after successful registration
        return render(request, 'app/customerregistration.html', {'form': form})







def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

#def login(request):
 #return render(request, 'app/login.html')



#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')




