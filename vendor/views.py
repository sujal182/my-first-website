from django.shortcuts import render , redirect
from .models import *
from ecom.models import *

# Create your views here.
def registration_ven(request):
    data = TYPE_BUSINESS
    if request.method == 'POST':
        sign_up = ven_reg(email = request.POST['email'],
                               name = request.POST['name'],
                               mob = request.POST['mob'],
                               add = request.POST['add'],
                               password = request.POST['password'],
                               sell_type = request.POST['bt'])
        try:
            already_reg = ven_reg.objects.get(email = request.POST['email'])
            if already_reg:
                return render(request,'vendor/register.html',{'already':"Email already exists.."})   
        except:
            sign_up.save()
            return render(request,'vendor/register.html',{'registration':"Registration successfull.",'type':data})
            #return redirect('login')
    else:
        return render(request,'vendor/register.html',{'type':data})
    
def ven_login(request):
    if request.method == 'POST':
        try:
            is_present = ven_reg.objects.get(email = request.POST['email'])
            if is_present:
                if request.POST['password'] == is_present.password:
                    request.session['ven_login'] = is_present.email
                    return redirect('ven_index')
                else:
                    return render(request,'vendor/ven_login.html',{'wrong_pass':"password is incorrect..."})
        except:
            return render(request,'vendor/ven_login.html',{'not_registered':"this email does not exists..."})
    else:
        return render(request,'vendor/ven_login.html')

def add_pro(request):
    cat = category.objects.all()
    if request.method == 'POST' and request.FILES:
        logged_in = ven_reg.objects.get(email = request.session['ven_login'])
        selected_cat = category.objects.get(name = request.POST['Category'])
        pro_store = Product(name = request.POST['Name'],
                            image = request.FILES['Image'],
                            discription = request.POST['Discrption'],
                            stock = request.POST['Stock'],
                            price  = request.POST['Price'],
                            category = selected_cat,
                            vendor = logged_in
                            )
        pro_store.save()
    return render(request,'vendor/add_pro.html',{'cat':cat})

def ven_index(request):
    if 'ven_login' in request.session:
        vendor = ven_reg.objects.get(email = request.session['ven_login'])
        pros = Product.objects.filter(vendor = vendor)
        return render(request,'cat_pro.html',{'pros':pros,'ven_logged_in':True})
    return render(request,'index.html')

def update_pro(request,id):
    pro = Product.objects.get(id = id)
    if request.method == 'POST':
        pro.name = request.POST['pro_name']
        pro.discription = request.POST['pro_des']
        pro.price = request.POST['pro_price']
        pro.stock = request.POST['pro_stock']
        pro.save()
        return render(request,'vendor/update_pro.html',{'product':pro})
    else:
        return render(request,'vendor/update_pro.html',{'product':pro})
