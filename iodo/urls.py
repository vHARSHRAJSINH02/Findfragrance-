from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
   path("", views.index, name="index.html"),
   path("basic", views.basic, name="basic.html"),
   path("contact", views.contact, name="contact.html"),
   path("login", views.signin, name="login"),
   path("register", views.register, name="register"),
   path("forgot", views.forgot, name="forgot"),
   path("viewdata", views.viewdata, name="viewdata"),
   path("checkuser", views.checklogin, name="checkuser"),
   path("logout", views.logout, name="logout"),
   path("forgotpassword", views.forgotpassword, name="forgotpassword"),
   path('shop', views.shop, name='shop'),
   path('completeprofile', views.completeprofile, name='completeprofile'),
   path('completeyourprofile', views.completeyourprofile, name='completeyourprofile'),
   path('yourprofile', views.yourprofile, name='yourprofile'),
   path("categorywiseproduct/<int:pcid>", views.categorywiseproduct, name="categorywiseproduct"),
   path("subcategorywiseproduct/<int:pscid>", views.subcategorywiseproduct, name="subcategorywiseproduct"),
   path("single/<int:myid>", views.productView, name="ProductDetail"),
   path("addtowishlist/<int:awid>", views.addtowishlist, name="addtowishlist"),
   path('wishlist', views.wishlists, name='wishlist'),
   path("removewish/<int:dwid>", views.removewish, name="removewish"),
   path("addtocart", views.addtocart, name="addtocart"),
   path('cart', views.Cart, name='cart'),
   path('payment', views.payment, name='payment'),
   path("removeitem/<int:did>", views.RemoveFromCart, name="RemoveFromCart"),
   path("order-complete", views.OrderComplete, name="OrderComplete"),
   path("verifypayment", views.verifypayment, name="verifypayment"),
   path("submitreview", views.SubmitReview, name="SubmitReview"),
   path("submitcontact", views.submitcontact, name="submitcontact"),
   path("yourorders", views.yourorders, name="yourorders"),
   path("yourordersingle/<int:yoid>", views.yourordersingle, name="yourordersingle"),
]
