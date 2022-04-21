from distutils.log import error
from sqlite3 import Date
from sys import flags
from tokenize import Special
from unicodedata import category
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password,check_password
from django.http import JsonResponse
from .models import  orders, cart as car,products,customer as cust


def get_customer(request):
    customer={}
    customer_id = request.session.get('customer')
    if customer_id:
        customer = cust.objects.get(id=customer_id)
    return customer


def Home(request):
    customer=get_customer(request)
    print(customer)
    return render(request, 'index.html',{'customer':customer})




def post_method_cart(request):
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity<=1:
                    cart.pop(product)
                else:
                    cart[product] = quantity-1
            else:
                cart[product] = quantity+1
        else:
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1
    request.session['cart'] = cart
    print(request.session['cart'])
    redirect('clothes')

def get_method_cart(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
# clothes
def clothes(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='clothes')
    return render(request, 'clothes.html', {'clothes': p,'customer':customer})


def men(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='clothes',productCategory='men' )
    return render(request, 'men.html', {'clothes': p,'customer':customer})


def women(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='clothes',productCategory='women' )
    return render(request, 'women.html', {'clothes': p,'customer':customer})


def kids(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='clothes',productCategory='kids' )
    return render(request, 'kids.html', {'clothes': p,'customer':customer})


# jewellery

def jewellery(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='jewellery' )
    return render(request, 'jewellery.html', {'jewellery': p,'customer':customer})


# furniture

def furniture(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        post_method_cart(request)

    get_method_cart(request)
    p=products.objects.filter(category='furniture' )
    return render(request, 'furniture.html', {'furniture': p,'customer':customer})


#validate Customer

def validate(fname,lname,email,phone,password):
    error=''
    if (not fname):
        error="First Name is Required!!"
    elif (len(fname)<4):
        error="First Name must have at least 4 characters"
    elif not lname:
        error="Last Name is Required!!"
    elif (len(lname)<4):
        error="Last Name must have at least 4 characters"
    elif(not phone):
        error="Phone Number is Required!!"
    elif(len(phone)<10):
        error="Phone Number must have 10 digits"
    elif(not email):
        error="Email is Required!!"
    elif(len(email)<12):
        error="Enter a valid email"
    elif(not password):
        error="Password is Required!!"
    elif(passwordValidate(password)==False):
        error="""Password must have at least 8 characters
        Password must contain atleast 1 uppercase character
        Password must contain atleast 1 digit
        Password must contain atleast 1 special character"""
    else:
        error=cust.isExists(email)
    return error

def passwordValidate(password):
    specialchars=['!','@','#','$','%','^','&','*','(',')','-','+','|','~',':',';','?','<','>',',','.']
    flag=0
    if len(password)<8:
        return False
    for i in password:
        if i>='A' and i<='Z':
            flag+=1
            break
    for i in password:
        if i>='0' and i<='9':
            flag+=1
            break
    for i in password:
        if i in specialchars:
            flag+=1
            break

    if(flag==3):
        return True
    return False



# customer

def customer(request):
    if request.method == 'GET':
        return render(request,'customer.html')
    else:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        values = {'fname':fname, 'lname':lname, 'phone':phone, 'email':email, 'password':password}
        error=validate(fname,lname, email, phone, password)

        if(len(error)>0):
            return render(request, 'customer.html', {'error': error,'values':values})
        else:
            hashpassword = make_password(password)
            x = cust(firstname=fname,lastname=lname,phone=phone, email=email, password=hashpassword)
            x.save()
            return redirect('Login')


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        values = {'email':email, 'password':password}
        customerr=cust.get_customer_by_email(email)
        error=None
        if customerr:
            flag=check_password(password,customerr.password)
            if flag:
                request.session['customer']=customerr.id
                request.session['email']=customerr.email
                request.session['cart']={}
                return redirect('Home')
            else:
                error="Email or Password invalid !!"
        else:
            error="Email or Password invalid !!"
        return render(request, 'login.html', {'error': error})


#cart

def cart(request):
    customer=get_customer(request)
    print(customer)
    if request.method == "POST":
        cart = request.session.get('cart')
        order=request.POST.get('order')
        if order!=None:
            address=request.POST.get('address')
            print(address)
            customer_id = request.session.get('customer')
            keys= cart.keys()
            orderprods = products.objects.filter(id__in=keys)
            print(cart)
            for prod in orderprods:
                cost=int(prod.cost)
                discount=int(prod.discount)
                quantity=(cart.get(str(prod.id)))
                price = (cost-cost*discount/100)*quantity
                price = round(price,2)
                customer=cust.objects.get(id=customer_id)
                dbobj=orders(customer=customer,product=prod,quantity=quantity,price=price,address=address)
                dbobj.save()
            request.session['cart'] ={}
            return redirect('clothes') 

        product = request.POST.get('product')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        redirect('cart')

    

    cart=request.session.get('cart')
    print(cart)
    keys=cart.keys()
    c=products.objects.filter(id__in=keys)
    return render(request, 'cart.html',{'products': c ,'customer':customer})


#orders

def yourorders(request):
    customer=get_customer(request)
    print(customer)
    customer_id = request.session.get('customer')
    customer = cust.objects.get(id=customer_id)
    o = orders.objects.filter(customer=customer).order_by('-date')
    return render(request, 'orders.html',{'orders':o,'customer':customer})


#logout 

def logout(request):
    request.session.clear()
    request.session['cart']={}
    return redirect('Login')
       