from django.shortcuts import render , HttpResponse , redirect 
from .models import *
from vendor import *
# Create your views here.


def first(request):
    return HttpResponse("this is my first view..")

def demo(request):
    return render(request,'demo.html')

def style(request):
    return render(request,'style.html')



def show(request):
    data = Student.objects.all()
    print(data)
    # for i in data:
    #     print(i.email)
    return render(request,'show.html',{'student':data})


def showimg(request):
    dataimg = Img.objects.all()
    return render(request,'showimg.html',{'dataimg':dataimg})


def store(request):
    if request.method == 'POST':
        print("this is first line after post method ")
        store_data = Student()
        store_data.email = request.POST['email']
        store_data.name = request.POST['uname']
        store_data.save()
    return render(request,'store.html')


def storeget(request):
    if request.method == 'GET':
        # store_data = Student()
        email = request.GET.get('email')
        name = request.GET.get('uname')
        # store_data.save()
        print(name,email)
    return render(request,'storeget.html')


def storeimg(request):
    if request.method == 'POST' and request.FILES:
        store_image = Img()
        store_image.name = request.POST['name']
        store_image.image = request.FILES['image']
        store_image.save()
    return render(request,'storeimg.html')


# filter - returns multiple matching queries
        # - if query not found then it does not give error 

# get - return only one unique data 
    # - if query not found then it returns error 
from django.contrib.auth.hashers import make_password , check_password


# def register(request):
    # if request.method == 'POST':
    #     encryptd_password = make_password(request.POST['password'])
    #     sign_up = Registration(email = request.POST['email'],
    #                            name = request.POST['name'],
    #                            mob = request.POST['mob'],
    #                            add = request.POST['add'],
    #                            password = encryptd_password
    #                            )
    #     try:
    #         already_reg = Registration.objects.get(email = request.POST['email'])
    #         if already_reg:
    #             return render(request,'register.html',{'already':"Email already exists.."})   
    #     except:
    #         sign_up.save()
    #         return render(request,'register.html',{'registration':"Registration successfull."})
    #         #return redirect('login')
    # else:
    #     return render(request,'register.html')
from.encrypt_pass import encrypt , decrypt

def register(request):
    if request.method == 'POST':
        encryptd_password = encrypt(request.POST['password'])
        sign_up = Registration(email = request.POST['email'],
                               name = request.POST['name'],
                               mob = request.POST['mob'],
                               add = request.POST['add'],
                               password = encryptd_password
                               )
        try:
            already_reg = Registration.objects.get(email = request.POST['email'])
            if already_reg:
                return render(request,'register.html',{'already':"Email already exists.."})   
        except:
            sign_up.save()
            return render(request,'register.html',{'registration':"Registration successfull."})
            #return redirect('login')
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        try:
            is_present = Registration.objects.get(email = request.POST['email'])
            if is_present:
                # password_true = check_password(request.POST['password'],is_present.password)
                dp = decrypt(is_present.password)
                if request.POST['password'] == dp:
                # if password_true:
                    # request.POST['password'] == is_present.password:
                    request.session['login'] = is_present.email
                    return redirect('index')
                else:
                    return render(request,'login.html',{'wrong_pass':"password is incorrect..."})
        except:
            return render(request,'login.html',{'not_registered':"this email does not exists..."})
    else:
        return render(request,'login.html')
    
def profile(request):
        if 'login' in request.session:
            logged_user = Registration.objects.get(email = request.session['login'])
            if request.method == 'POST':
                # update_user = logged_user(name = request.POST['name'],
                #             mob = request.POST['mob'],
                #             add = request.POST['add']  )
                logged_user.name = request.POST['name']
                logged_user.add = request.POST['add']
                logged_user.mob = request.POST['mob']
                logged_user.save()
                # return render(request,'profile.html',{'logged_in':True,'logged_user':logged_user})
                return redirect('profile')
            else:
                return render(request,'profile.html',{'logged_in':True,'logged_user':logged_user})
        else:
            return redirect('login')
    # else:
    #     return redirect('login')

def index(request):
    cat = category.objects.all()
    if 'login' in request.session:
        print(1)
        return render(request, 'index.html', {'cat': cat, 'logged_in': True})
    elif 'ven_login' in request.session:
        print(2)
        return render(request, 'index.html', {'ven_logged_in': True})
    else:
        return render(request, 'index.html', {'cat': cat})

def logout(request):
    if 'login' in request.session:
        del request.session['login']
        return redirect('index')
    elif 'ven_login' in request.session:
        del request.session['ven_login']
        return redirect('index')

        

def cat_pro(request,id):
    pro = Product.objects.filter(category = id)
    if 'login' in request.session:
        return render(request,'cat_pro.html',{'pro':pro,'logged_in':True})
    else:
        return render(request,'cat_pro.html',{'pro':pro})


def pro_details(request,id):
    prod = Product.objects.get(pk = id)
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session['login'])
        # if request.method == 'POST':
        if 'buy' in request.POST:
            if int(request.POST['qty']) > prod.stock:
                return render(request,'product.html',{'logged_in':True,'product':prod,'less_stock':True})
            else:
                request.session['qty'] = request.POST['qty']
                request.session['proid'] =  id
                return redirect('checkout')
        elif 'cart' in request.POST:
            add_to_cart = Cart(user = logged_in,
                 pro = prod,
                 qty = request.POST['qty'],
                 total_price = prod.price * int(request.POST['qty'])
                 )
            add_to_cart.save()
            return render(request,'product.html',{'logged_in':True,'product':prod})
        else:
            return render(request,'product.html',{'logged_in':True,'product':prod})
    else:
        return render(request,'product.html',{'product':prod})


def cart_view(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session['login'])
        cart_data = Cart.objects.filter(user = logged_in,order_id = 0)
        total = 0
        for i in cart_data:
            total += i.total_price
        return render(request,'cart.html',{'logged_in':True,'cart':cart_data,'total':total})
    else:
        return redirect('login')

def plus_pro(request,id):
    cart_data = Cart.objects.get(id = id)
    # pro = Product.objects.get(id = cart_data.pro)
    cart_data.qty += 1
    cart_data.total_price += cart_data.pro.price
    cart_data.save()
    return redirect('cart_view')


def minus_pro(request,id):
    cart_data = Cart.objects.get(id = id)
    if cart_data.qty <= 1:
        cart_data.delete()
        return redirect('cart_view')
    else:
        cart_data.qty -= 1
        cart_data.total_price -= cart_data.pro.price
        cart_data.save()
        return redirect('cart_view')

def checkout_cart(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session['login'])
        cart_data = Cart.objects.filter(user = logged_in,order_id = 0)
        total = 0
        for i in cart_data:
            total += i.total_price
        if request.method == 'POST':
            if request.POST['paymentvia'] == 'cod':
                for i in cart_data:
                    obj = Order()
                    obj.user = logged_in
                    obj.pro = i.pro
                    obj.qty = i.qty
                    obj.name = request.POST['name']
                    obj.mob = request.POST['mob']
                    obj.add = request.POST['add']
                    obj.city = request.POST['city']
                    obj.state = request.POST['state'] 
                    obj.pin = request.POST.get('pin')
                    obj.payment_type = request.POST['paymentvia']
                    obj.payment_id = "cod"
                    obj.total_price = i.total_price
                    obj.save()
                    latest_order = Order.objects.latest('id')
                    i.order_id = latest_order.id
                    i.save()
                return redirect('index')
            else:
                request.session['cart_amount'] = total
                request.session['from_cart'] = True
                request.session['name'] = request.POST['name']
                request.session['mob'] = request.POST['mob']
                request.session['add'] = request.POST['add']
                request.session['city'] = request.POST['city']
                request.session['state'] = request.POST['state']
                request.session['pin'] = request.POST['pin']
                return redirect('razorpayment')
        else:
            return render(request,'checkout.html',{'logged_in':logged_in,'cart_data':cart_data,'total':total})
    else:
        return render(request,'checkout.html')


def checkout(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session['login'])
        pro = Product.objects.get(id =  request.session['proid'])
        if request.method == 'POST':
            if request.POST['paymentvia'] == 'cod':
                obj = Order(user = logged_in,
                            pro = pro,
                            qty = request.session['qty'],
                            name = request.POST['name'],
                            mob = request.POST['mob'],
                            add = request.POST['add'],
                            city = request.POST['city'],
                            state = request.POST['state'] ,
                            pin = request.POST['pin'],
                            payment_type = request.POST['paymentvia'],
                            payment_id = "cod",
                            total_price = pro.price * int(request.session['qty'])
                            )
                obj.save()
                pro.stock -= int(request.session['qty'])
                pro.save()
                return redirect('index')
            else:
                request.session['amount'] = pro.price * int(request.session['qty'])
                request.session['name'] = request.POST['name']
                request.session['mob'] = request.POST['mob']
                request.session['add'] = request.POST['add']
                request.session['city'] = request.POST['city']
                request.session['state']  = request.POST['state'] 
                request.session['pin'] = request.POST['pin']
                return redirect('razorpayment')
        else:
            return render(request,'checkout.html',{'logged_in':logged_in})
    else:
        return redirect('login')
    


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razorpayment(request):
    if 'from_cart' in request.session:
        del request.session['from_cart']
        currency = 'INR'
        amount = int(request.session['cart_amount']) * 100
        razorpay_order = razorpay_client.order.create(dict(
            currency = currency,
            amount =  amount,
            payment_capture = '0'
        ))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/payment_handler_cart/'
        return render(request,'razorpay.html',{'razorpay_merchant_key':settings.RAZORPAY_KEY_ID,
                                            'razorpay_amount':amount,
                                            'currency':currency,
                                            'razorpay_order_id':razorpay_order_id,
                                            'callback_url' : callback_url})
    else:
        currency = 'INR'
        amount = int(request.session['amount']) * 100
        razorpay_order = razorpay_client.order.create(dict(
            currency = currency,
            amount =  amount,
            payment_capture = '0'
        ))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/payment_handeler/'
        return render(request,'razorpay.html',{'razorpay_merchant_key':settings.RAZORPAY_KEY_ID,
                                            'razorpay_amount':amount,
                                            'currency':currency,
                                            'razorpay_order_id':razorpay_order_id,
                                            'callback_url' : callback_url})

@csrf_exempt
def payment_handler_cart(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            param_dict = {'razorpay_payment_id' : payment_id,
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_signature' : signature}
            razorpay_client.utility.verify_payment_signature(param_dict)
            amount = int(request.session['cart_amount']) * 100
            razorpay_client.payment.capture(payment_id, amount)
            logged_in = Registration.objects.get(email = request.session['login'])
            cart_data = Cart.objects.filter(user = logged_in,order_id = 0)
            for i in cart_data:
                obj = Order()
                obj.user = logged_in
                obj.pro = i.pro
                obj.qty = i.qty
                obj.name = request.session['name']
                obj.mob = request.session['mob']
                obj.add = request.session['add']
                obj.city = request.session['city']
                obj.state = request.session['state'] 
                obj.pin = request.session.get('pin')
                obj.payment_type = "online"
                obj.payment_id = payment_id
                obj.total_price = i.total_price
                obj.save()
                latest_order = Order.objects.latest('id')
                i.order_id = latest_order.id
                i.save()
            return redirect('index')
        except Exception as e:
            print(e,"eeeeeerrrrrrrrrrooooooorrrrr")
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



@csrf_exempt
def payment_handeler(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            param_dict = {'razorpay_payment_id' : payment_id,
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_signature' : signature}
            razorpay_client.utility.verify_payment_signature(param_dict)
            amount = int(request.session['amount']) * 100
            razorpay_client.payment.capture(payment_id, amount)
            logged_in = Registration.objects.get(email = request.session['login'])
            pro = Product.objects.get(id = request.session['proid'])
            store_order = Order(user = logged_in,
                  pro = pro,
                  qty = request.session['qty'],
                  name = request.session['name'],
                  mob = request.session['mob'],
                  add = request.session['add'],
                  city = request.session['city'],
                  state = request.session['state'],
                  pin = request.session['pin'],
                  total_price = request.session['amount'],
                  payment_type = 'online',
                  payment_id = payment_id
                  )
            store_order.save()
            pro.stock -= int(request.session['qty'])
            pro.save()
            return redirect('index')
        except Exception as e:
            print(e,"eeeeeerrrrrrrrrrooooooorrrrr")
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

from django.core.mail import send_mail
import random

def email_send(request):
    otp = random.randint(100,999)
    request.session['otp'] = otp
    if request.method == 'POST':
        email = request.POST['email']
        send_mail(
            'Checking mail',
            f'Your otp is {otp}',
            'pqr6997@gmail.com',
            [email],
            fail_silently = False
        )
        # return render(request,'send_email.html')
        return redirect('send_otp')
    else:
        return render(request,'send_email.html')



def send_otp(request):
    if request.method == 'POST':
        if request.session['otp'] == int(request.POST['otp']):
            return redirect('index')
        else:
            return render(request,'check_otp.html',{'incorrect':"Invalid otp"})
    else:
        return render(request,'check_otp.html')
