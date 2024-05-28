from django.shortcuts import render, redirect
from django.contrib import messages
from .models import login
from .models import product_detail
from .models import customer_detail
from .models import area
from .models import city
from .models import state
from .models import product_category
from .models import product_subcategory
from .models import product_wishlist
from .models import product_cart
from .models import product_order
from .models import card_detail
from .models import FEEDBACK_TABLE
from .models import feedback
# Create your views here.

from django.http import HttpResponseRedirect

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)


def index(request):
  try:
    uid = request.session['log_id']
    productsview = product_detail.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    pdata = {
      'productsview': productsview,
      'profiledata': profiledata,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
    }
    return render(request, 'index.html', pdata)
  except:
    pass
  productsview = product_detail.objects.all()

  details = {
    'productsview': productsview,
  }

  return render(request, 'index.html', details)

def basic(request):
    return render(request, 'basic.html')

def contact(request):
    return render(request, 'contact.html')

def signin(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def completeprofile(request):
  try:
    uid = request.session['log_id']
    productsview = product_detail.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    orderdata = product_order.objects.filter(L_id=login(id=uid))

    pdata = {
      'productsview': productsview,
      'profiledata': profiledata,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'orderdata': orderdata,
    }
    return render(request, 'completeprofile.html', pdata)
  except:
    pass
  productsview = product_detail.objects.all()

  details = {
    'productsview': productsview,
  }
  return render(request, 'completeprofile.html', details)

def completeyourprofile(request):
  uid = request.session['log_id']
  if request.method == 'POST':
    uname = request.POST.get("name")
    uaddress = request.POST.get("address")
    udob = request.POST.get("dob")
    file = request.FILES['dp']
    uarea = request.POST.get("areaname")
    ucity = request.POST.get("cityname")
    ustate = request.POST.get("statename")

    userdata = customer_detail(L_id=login(id=uid), Name=uname, Dob=udob, Address=uaddress, dp=file,
                               Area_id=area(id=uarea), City=city(id=ucity), State_id=state(id=ustate))
    userdata.save()
    messages.success(request, 'Data Inserted Successfully.')
    return redirect(index)
  else:
    messages.error(request, 'error occured')

def yourprofile(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,

    }
    return render(request, 'yourprofile.html', details)
  except:
    pass
  return render(request, 'yourprofile.html')

def forgot(request):
    return render(request, 'forgot.html')


def payment(request):
  return render(request, 'payment.html')


def viewdata(request):
  if request.method == 'POST':
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    password = request.POST.get("confirmpassword")

    logindata = login(Email=email, Phone=phone, Password=password, Role="USER", Status="1")
    logindata.save()
    messages.success(request, 'Data Inserted Successfully. you can login now')
  else:
    messages.error(request, 'error occured')

  return redirect(index)

def checklogin(request):
  if request.method == 'POST':
    username = request.POST['email']
    password = request.POST['password']
    try:
      user = login.objects.get(Email=username, Password=password)
      request.session['log_user'] = user.Email
      request.session['log_id'] = user.id
      request.session.save()

    except login.DoesNotExist:
      user = None

    if user is not None:
      print("successfully logged in")
      messages.success(request, 'Successfully Logged In')
      redirect(index)

    else:
      print("not logged in")
      messages.error(request, 'Invalid USER ID')
  return redirect(index)

def logout(request):
    try:
        del request.session['log_user']
        del request.session['log_id']
    except:
        pass
    return redirect(index)

def forgotpassword(request):
  if request.method == 'POST':
    username = request.POST['email']
    try:
      user = login.objects.get(Email=username)

    except login.DoesNotExist:
      user = None
    # if user exist then only below condition will run otherwise it will give error as described in else condition.
    if user is not None:
      #################### Password Generation ##########################
      import random
      letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
      numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
      symbols = ['!', '#', '$', '%', '&', '*']

      nr_letters = 6
      nr_symbols = 1
      nr_numbers = 3
      password_list = []

      for char in range(1, nr_letters + 1):
        password_list.append(random.choice(letters))

      for char in range(1, nr_symbols + 1):
        password_list += random.choice(symbols)

      for char in range(1, nr_numbers + 1):
        password_list += random.choice(numbers)

      print(password_list)
      random.shuffle(password_list)
      print(password_list)

      password = ""  # we will get final password in this var.
      for char in password_list:
        password += char

      ##############################################################

      msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

      ############ code for sending mail ########################

      from django.core.mail import send_mail

      send_mail(
        'Your New Password',
        msg,
        'divybavishi001@gmail.com',
        [username],
        fail_silently=False,
      )
      # NOTE: must include below details in settings.py
      # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
      # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      # EMAIL_HOST = 'smtp.gmail.com'
      # EMAIL_USE_TLS = True
      # EMAIL_PORT = 587
      # EMAIL_HOST_USER = 'mail from which email will be sent'
      # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

      #############################################

      # now update the password in model
      cuser = login.objects.get(Email=username)
      cuser.Password = password
      cuser.save(update_fields=['Password'])

      print('Mail sent')
      messages.info(request, 'mail is sent')
      return redirect(index)

    else:
      messages.info(request, 'This account does not exist')
  return redirect(index)

def shop(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    productsview = product_detail.objects.all()

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.all()

    # Paginate items
    items_per_page = 4
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'items_page': items_page
    }

    return render(request, 'shop.html', pdata)
  except:
    pass
  productdetails = product_detail.objects.all()
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.all()

  # Paginate items
  items_per_page = 4
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)
  details = {
    'productdetails': productdetails,
    'items_page': items_page,
  }
  return render(request, 'shop.html', details)

def categorywiseproduct(request, pcid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

    # Paginate items
    items_per_page = 3
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'productdetails': productdetails,
      'items_page': items_page,

    }
    return render(request, 'categorywiseproduct.html', details)
  except:
    pass
  productdetails = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.filter(Pro_Cat=product_category(id=pcid))

  # Paginate items
  items_per_page = 3
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)

  details = {
    'productdetails': productdetails,
    'items_page': items_page,
  }
  return render(request, 'categorywiseproduct.html', details)

def subcategorywiseproduct(request, pscid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    default_page = 1
    page = request.GET.get('page', default_page)

    # Get queryset of items to paginate
    items = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

    # Paginate items
    items_per_page = 3
    paginator = Paginator(items, items_per_page)

    try:
      items_page = paginator.page(page)
    except PageNotAnInteger:
      items_page = paginator.page(default_page)
    except EmptyPage:
      items_page = paginator.page(paginator.num_pages)

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'productdetails': productdetails,
      'items_page': items_page,

    }
    return render(request, 'subcategorywiseproduct.html', details)
  except:
    pass
  productdetails = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))
  default_page = 1
  page = request.GET.get('page', default_page)

  # Get queryset of items to paginate
  items = product_detail.objects.filter(Pro_Subcat=product_subcategory(id=pscid))

  # Paginate items
  items_per_page = 3
  paginator = Paginator(items, items_per_page)

  try:
    items_page = paginator.page(page)
  except PageNotAnInteger:
    items_page = paginator.page(default_page)
  except EmptyPage:
    items_page = paginator.page(paginator.num_pages)

  details = {
    'productdetails': productdetails,
    'items_page': items_page,
  }
  return render(request, 'subcategorywiseproduct.html', details)


def productView(request, myid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    productdetails = product_detail.objects.get(id=myid)

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'productdetails': productdetails,

    }
    return render(request, 'single.html', details)
  except:
    pass
  productdetails = product_detail.objects.get(id=myid)
  details = {
    'productdetails': productdetails,
  }
  return render(request, 'single.html', details)

def addtowishlist(request, awid):
  uid = request.session['log_id']

  try:
    wl = product_wishlist.objects.get(Product_id=product_detail(id=awid), L_id=login(id=uid))

  except product_wishlist.DoesNotExist:
    wl = None

  if wl is None:
    wldata = product_wishlist(Product_id=product_detail(id=awid), L_id=login(id=uid))
    wldata.save()
    messages.success(request, 'Added to Wishlist.')
  else:
    messages.error(request, 'Already added to Wishlist.')

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def wishlists(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    wishlistdata = product_wishlist.objects.filter(L_id=uid)

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'wishlistdata': wishlistdata,
    }

    return render(request, 'wishlist.html', pdata)
  except:
    pass
  return render(request, 'wishlist.html')

def removewish(request, dwid):
  product_wishlist.objects.filter(Product_id=product_detail(id=dwid)).delete()

  return redirect(wishlists)

def addtocart(request):
  try:
    if request.session.is_empty():
      messages.error(request, "Please login")
      return redirect(index)
    else:
      try:
        if request.method == 'POST':
          cartname = request.POST.get("pname")
          cartprice = request.POST.get("amount")
          cartquantity = request.POST.get("quant[1]")
          proid = request.POST.get("pid")
          finalprice = int(cartprice) * int(cartquantity)

          uid = request.session['log_id']
          print(uid)

          cartdata = product_cart(Product_id=product_detail(id=proid), L_id=login(id=uid), Product_name=cartname,
                                  Price=cartprice, Quantity=cartquantity,
                                  Final_price=finalprice)
          print("check1")
          cartdata.save()
          messages.success(request, 'Product is added to Cart.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
        pass
      messages.error(request, "Please login")
      return redirect(index)
  except:
    pass
  messages.error(request, "Please login")
  return redirect(index)

from django.db.models import Sum

def Cart(request):
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
        profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
        profiledata = None

    # cartitems = CART_TABLE.objects.all()
    cartitems = product_cart.objects.filter(L_id=uid, Order_status=0)

    carttotal = product_cart.objects.filter(L_id=uid, Order_status=0).aggregate(Sum("Final_price"))
    carttotal = carttotal.get("Final_price__sum")

    print(carttotal)
    uname = customer_detail.objects.filter(L_id=login(id=uid))

    cartview = {
        'cartitems': cartitems,
        'carttotal': carttotal,
        'uname': uname,
        'logdetail': logdetail,
        'statedetail': statedetail,
        'citydetail': citydetail,
        'areadetail': areadetail,
        'profiledata': profiledata,
    }

    return render(request, 'cart.html', cartview)


def RemoveFromCart(request, did):
  product_cart.objects.filter(id=did).delete()

  cartitems = product_cart.objects.all()
  carttotal = product_cart.objects.aggregate(Sum("Final_price"))
  carttotal = carttotal.get("Final_price__sum")

  print(carttotal)
  uid = request.session['log_id']
  uname = customer_detail.objects.filter(L_id=login(id=uid))

  context = {
    'cartitems': cartitems,
    'carttotal': carttotal,
    'uname': uname,
  }

  return redirect(Cart)

def OrderComplete(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    address = request.POST.get("address")
    uid = request.session['log_id']
    cust_detail = customer_detail.objects.get(L_id=login(id=uid))

    if address == "":
      address = cust_detail.Address

    paymentopt = request.POST.get("payment")
    print(paymentopt)
    if paymentopt == "online":
      return render(request, 'payment.html')
    else:

      carttotal = product_cart.objects.filter(L_id=uid, Order_status=0).aggregate(Sum("Final_price"))
      carttotal = carttotal.get("Final_price__sum")
      orderdata = product_order(L_id=login(id=uid), Address=address, Total_amount=carttotal,
                                Payment_status=paymentopt, order_status=0)
      orderdata.save()

      lasstid = product_order.objects.latest('id')

      print(lasstid)

      objid = lasstid.id
      print(objid)

      obj = product_cart.objects.filter(L_id=login(id=uid), Order_status=0)
      for object in obj:
        object.Order_id = objid
        object.Order_status = 1
        object.save()

      messages.success(request, 'Order Placed Successfully.')
      return render(request, 'orderplaced.html')

def verifypayment(request):
  if request.method == 'POST':
    name = request.POST.get("name")
    card_number = request.POST.get("number")
    card_cvv = request.POST.get("security-code")
    exp_date = request.POST.get("expiration-month-and-year")

    carddetail = card_detail.objects.get()

    ocn = carddetail.card_number
    ocvv = carddetail.card_cvv
    oexpd = carddetail.exp_date
    cb = carddetail.card_balance
    carttotal = product_cart.objects.aggregate(Sum("Final_price"))
    carttotal = carttotal.get("Final_price__sum")

    if ocn == card_number and ocvv == card_cvv and oexpd == exp_date:
      print("payment expected")
      cb = cb - carttotal
      carddetail.card_balance = cb
      carddetail.save(update_fields=['card_balance'])
      uid = request.session['log_id']
      cust_detail = customer_detail.objects.get(L_id=login(id=uid))
      custadd = cust_detail.Address
      orderdata = product_order(L_id=login(id=uid), Address=custadd, Total_amount=carttotal,
                                Payment_status="online", order_status=0)
      orderdata.save()

      lasstid = product_order.objects.latest('id')

      print(lasstid)

      objid = lasstid.id
      print(objid)

      obj = product_cart.objects.filter(L_id=login(id=uid))
      for object in obj:
        object.Order_id = objid
        object.Order_status = 1
        object.save()

      messages.success(request, 'Payment Successfull.')
      return render(request, 'orderplaced.html')

    else:
      messages.error(request, 'Payment failed. Wrong payment details')
      return redirect(Cart)

  return render(request, 'payment.html')

def SubmitReview(request):
  uid = request.session['log_id']
  if request.method == 'POST':
    ratings = request.POST.get("input-1")
    feedback = request.POST.get("feedback")
    print(ratings)
    print(feedback)
    subreview = FEEDBACK_TABLE(L_ID=login(id=uid), RATINGS=ratings, COMMENT=feedback)
    subreview.save()

  return redirect(index)

def submitcontact(request):
  if request.method == 'POST':
    name = request.POST.get("Name")
    email = request.POST.get("Sender")
    comment = request.POST.get("Message")

    subreview = feedback(Name=name, Email=email, Comment=comment)
    subreview.save()
    messages.success(request, 'Your response recorded Successfully.')

  return redirect(contact)

def yourorders(request):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    orderdata = product_order.objects.filter(L_id=login(id=uid))

    pdata = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'orderdata': orderdata,
    }

    return render(request, 'yourorders.html', pdata)
  except:
    pass
  return render(request, 'yourorders.html')


def yourordersingle(request, yoid):
  try:
    uid = request.session['log_id']
    logdetail = login.objects.all()
    statedetail = state.objects.all()
    citydetail = city.objects.all()
    areadetail = area.objects.all()
    cartdetail = product_cart.objects.filter(Order_id=yoid)

    try:
      profiledata = customer_detail.objects.get(L_id=uid)
    except customer_detail.DoesNotExist:
      profiledata = None

    details = {
      'logdetail': logdetail,
      'statedetail': statedetail,
      'citydetail': citydetail,
      'areadetail': areadetail,
      'profiledata': profiledata,
      'cartdetail': cartdetail,

    }
    return render(request, 'yourordersingle.html', details)
  except:
    pass

  return render(request, 'yourordersingle.html')