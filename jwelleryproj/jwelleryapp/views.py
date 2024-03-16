import razorpay
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse  # for json response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Address
from .models import Jproduct
from .models import Order
from .models import UserCart


# Create your views here.

def home(request):
    context = {}
    context = handle_nav(request, context)
    print(context, "rutuja")
    return render(request, "index.html", context)


def product(request):
    print(request)
    cat = request.GET.get('cat')
    print(cat)
    context = {}
    uid = request.user.id
    if cat is not None:
        product = Jproduct.objects.filter(cat=cat, is_active=True)
    else:
        product = Jproduct.objects.filter(is_active=True)

    context['prod'] = product
    context = handle_nav(request, context)
    print(context)
    return render(request, 'index.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            id = request.POST['prod_id']
            redirect_path = request.POST['redirect_path'] if 'redirect_path' in request.POST else None
            product = Jproduct.objects.get(id=id)
            user_id = request.user
            # if product already in cart then increase quantity
            cart = UserCart.objects.filter(user=user_id, product=product, order_id=None)
            if cart:  # if cart is exist then increase quantity
                print("cart exist")
                cart = cart[0]
                cart.quantity += 1
                cart.total += product.price
                cart.save()
            # if product not in cart then add product to cart
            else:
                print("cart not exist")
                # if cart does not exist then create new cart
                quantity = 1
                total = product.price * int(quantity)
                cart = UserCart(user=user_id, product=product, quantity=quantity, total=total, order_id=None)
                cart.save()

            if redirect_path:
                print(redirect_path, "helooooooooooooooooooo")
                return redirect(redirect_path)
            else:
                return redirect('products/' + id)
        else:
            return redirect('login?message=Please login to add product to cart')
    else:
        return redirect('login')
    pass


def user_login(request):
    context = {}
    if request.method == 'POST':
        user_name = request.POST['uname']
        user_pass = request.POST['upass']
        if user_name == ' ' or user_pass == '':
            context['errmsg'] = "Filed cannot be empty!!!"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=user_name, password=user_pass)
            if u is not None:  # if login page is not none all data username and password is present
                login(request, u)
                print(request.user.is_authenticated)
                return redirect('/')

            else:
                context['errmsg'] = "invalid username and password!!!"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    # print(request.user.is_authenticated)
    return redirect("/")


def register(request):
    context = {}
    if request.method == "POST":
        name = request.POST['uname']
        upass1 = request.POST['pass1']
        upass2 = request.POST['pass2']

        if name == ' ' or upass1 == '' or upass2 == '':
            context['errmsg'] = "Feild cannot be empty!!!"
            return render(request, 'register.html', context)
        elif upass1 != upass2:
            context['errmsg'] = "Password and Confirm password not matched!!!"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(username=name, email=name, password=upass1)
                u.set_password(upass1)
                u.save()
                context['success'] = "register succesfully!!!"
                return render(request, 'register.html', context)
            except Exception:
                context['errmsg'] = "Username already exist!!!"
                return render(request, 'register.html', context)
    else:
        return render(request, "register.html")


def product_detail(request, id):
    context = {}  # details in this we are going to give html/UI
    product = Jproduct.objects.get(id=id)  # product detail id= product id
    context['prod'] = product
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
        context['is_logged_in'] = True
        user_id = request.user.id
        cart = UserCart.objects.filter(user_id=user_id, product_id=id, order_id=None)
        context['cart'] = cart
    else:
        context['is_logged_in'] = False
    context = handle_nav(request, context)
    print(context)
    return render(request, 'product_details.html', context)


def handle_nav(request, context):  # fuction for checking user is login or not
    if request.user.is_authenticated:
        context['is_logged_in'] = True
        items = UserCart.objects.filter(user_id=request.user.id, order=None)
        length = len(items)
        context['cart_count'] = length  # cart_count is the variable in html
    else:
        context['is_logged_in'] = False
    return context


def user_cart(request):
    context = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        items = getcart(request.user)
        print(list(items))
        if items:
            context['items'] = items
            total = 0
            for i in items:
                total += i['total']
            context['total'] = total
    else:
        return redirect('/login')
    context = handle_nav(request, context)
    print(context, "tanu")
    return render(request, "user_cart.html", context)


def remove_from_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print(request.POST, "adyaaaaaaaaaaaaaa")
            user = request.user
            method = ""

            if 'product_id' in request.POST and 'quantity' in request.POST:  # it checks post request has product id and quantity then remove quantity wise
                method = "single"

                product_id = request.POST['product_id'][0]
                # fetch product from database
                product = Jproduct.objects.get(id=product_id)
                quantity = request.POST['quantity'][0]
                print(product_id, quantity, "tanuuuuuuuuuuuuuuu")
                handle_remove(product, user)

            elif 'product_id' in request.POST:  # if only product id is present then remove product
                method = 'singleproduct'
                print(request.POST)
                product_id = request.POST['product_id'][0]
                print(product_id)
                handle_remove_product(product_id, user)
            else:
                method = "all"
                all_remove(user)
            return redirect('/cart')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


def handle_remove_product(product_id, user):  # function for remove product full
    cart = UserCart.objects.filter(user=user, product_id=product_id, order_id=None)
    if cart:  # if product is present then delete product
        cart.delete()  # If the product is in the cart, this line deletes the cart object from the database, that is removing the product from the cart.
        return True
    else:
        return False


def handle_remove(product, user):  # function for remove product from cart quatity wise
    cart = UserCart.objects.filter(user=user, product=product, order_id=None)
    print(product, user, "tangiiiiii")
    if cart:
        cart = cart[0]
        if int(cart.quantity) > 1:  # if quantity is greater than 1 then decrease quantity
            cart.quantity -= 1
            print(cart.quantity, "pandiiii")
            cart.total -= cart.product.price
            cart.save()
        else:
            cart.delete()  # if quantity is 1 then delete product
        return True
    else:
        return False


def all_remove(user):
    cart = UserCart.objects.filter(user=user, order_id=None)
    if cart:
        cart.delete()
        return True
    else:
        return False


# create a fuction for search product
def search_product(request):
    context = {}
    if request.method == 'GET':
        search = request.GET['search']
        products = Jproduct.objects.filter(name__icontains=search)
        context['prod'] = products
        # return data in http response format
        data = list(products.values())
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'No data found'}, safe=False)


def getcart(user, getList=True):  # function for get cart details it will return list of cart items
    cart = UserCart.objects.filter(user=user, order_id=None).select_related('product').values('id',
                                                                                              'product__name',
                                                                                              'product__price',
                                                                                              'quantity', 'total',
                                                                                              'product__id',
                                                                                              'product__p_img',
                                                                                              'product__product_details',
                                                                                              'quantity', 'total')

    if getList:
        cart = list(cart)
    print("items found", len(list(cart)))
    return cart


def order(request):  # to go for payment
    if request.method != 'POST':
        return redirect('/login')
    else:
        user = request.user
        items = getcart(user)

        address_id = request.POST['address']
        address = Address.objects.get(id=address_id)
        payment_id = make_payment(items, user, address)

        if not payment_id:
            return HttpResponse("Payment failed")
        else:
            return redirect('/payment/' + payment_id)


def show_payment(request, payment):  # function for show payment details
    if request.user.is_authenticated:
        payment_info = Order.objects.get(orderid=payment)  # get payment details from order table using payment id
        context = {}
        context['payment_info'] = payment_info
        print(payment_info, "payment_info")
        return render(request, 'pay.html', context)
    else:
        return redirect('/login')


def get_order(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        items = getcart(user)
        subtotal = 0
        for i in items:
            n = i['product__price']
            subtotal += n
        context['subtotal'] = subtotal
        context['items'] = items
        context['address'] = Address.objects.filter(user=user)
    else:
        return redirect('/login')
    context = handle_nav(request, context)
    print(context, 'context here')
    return render(request, "placeorder.html", context)


def createAddress(request):  # function for create address
    if request.method == 'POST':
        user = request.user  # get user from request
        address = request.POST['address']
        phone = request.POST['phone_number']
        address = Address(user=user, address=address, phone_number=phone)
        address.save()
        return redirect('/placeorder')
    else:
        return redirect('/login')


def make_payment(items, user, address):  # function for payment     # items is the list of cart items
    test_key = settings.RAZORPAY_KEY_ID
    test_secret = settings.RAZORPAY_KEY_SECRET
    client = razorpay.Client(auth=(test_key, test_secret))
    sum = 0
    for i in items:
        sum += i['total']
    data = {"amount": sum * 100, "currency": "INR", "receipt": "order_rcptid_11"}
    try:

        payment = client.order.create(data=data)
        print(payment, "Meowwwwwwwwwww")
        # generate order in orders table
        order = Order(orderid=payment['id'], userid=user, address=address, amt=sum, paymentstatus='created') # orderid is the payment id 

        if order is None:
            return "Error enable to create order"

        order.save()
        # add order id to user cart table
        print(items, "items")
        for i in items:
            print(i['id'])
            cart = UserCart.objects.get(id=i['id'])
            cart.order = order
            cart.save()

        return payment['id']
    except Exception as e:
        print(e)
        return "Error", str(e)


@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        print(request.POST, "tannnngggyyyy")
        payment_id = request.POST['razorpay_payment_id']
        # fetch payment information
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.payment.fetch(payment_id)
        if payment is None:
            return HttpResponse('failure')

        print(payment, "pandaaaaaaa")
        # update payment status in order table
        order = Order.objects.get(orderid=payment['order_id'])
        order.paymentstatus = payment['status']
        order.save()
            
        # send mail to user for payment success
        user = order.userid
        #converting model object to dictionary
        # order=order.__dict__

        payment['amount']=payment['amount']/100
        message = f"Dear {user.username},\n\nThank you for your payment. Your payment of {payment['amount']} INR has been successfully processed.\n\nWe appreciate your business and look forward to serving you again.\n\nBest regards,\nThe Abhushan Jewellery Team"
        subject = 'Abhushan Jewellery Payment Success'
        send_mail(subject, message, 'rutuja.adsul31@gmail.com', [user.email])
        context={"amount":payment['amount'],"status":payment['status']}

        return render(request, 'paymentsuccess.html',context)
    else:
        return HttpResponse('failure')

