from django.db import models
from django.utils.safestring import mark_safe
from django.contrib import messages


# Create your models here.
class login(models.Model):
    Email = models.EmailField()
    Password = models.CharField(max_length=25)
    Phone = models.BigIntegerField()

    role = (
        ("ADMIN", "ADMIN"),
        ("USER", "USER"),
    )
    Role = models.CharField(max_length=10, choices=role)
    status = (
        ("0", "INACTIVE"),
        ("1", "ACTIVE")
    )
    Status = models.CharField(max_length=10, choices=status)

    def __str__(self):
        return self.Email


class state(models.Model):
    State_name = models.CharField(max_length=25)

    def __str__(self):
        return self.State_name


class city(models.Model):
    City_name = models.CharField(max_length=25)
    State_id = models.ForeignKey(state, on_delete=models.CASCADE)

    def __str__(self):
        return self.City_name


class area(models.Model):
    Area_name = models.CharField(max_length=25)
    City_id = models.ForeignKey(city, on_delete=models.CASCADE)
    STATE = models.ForeignKey(state, on_delete=models.CASCADE)

    def __str__(self):
        return self.Area_name


class customer_detail(models.Model):
    Name = models.CharField(max_length=25)
    L_id = models.ForeignKey(login, on_delete=models.CASCADE)
    Dob = models.DateField()
    Address = models.CharField(max_length=128)
    dp = models.ImageField(upload_to="photos", default="mydp.jpeg")

    def customer_photos(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.dp.url))

    customer_photos.allow_tags = True

    Area_id = models.ForeignKey(area, on_delete=models.CASCADE)
    City = models.ForeignKey(city, on_delete=models.CASCADE)
    State_id = models.ForeignKey(state, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class product_category(models.Model):
    Product_category_name = models.CharField(max_length=25)

    def __str__(self):
        return self.Product_category_name

class product_subcategory(models.Model):
    Product_subcategory_name = models.CharField(max_length=50)
    Product_cat = models.ForeignKey(product_category, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.Product_subcategory_name


class product_detail(models.Model):
    Pro_name = models.CharField(max_length=25)
    Pro_Cat = models.ForeignKey(product_category, on_delete=models.CASCADE, default="")
    Pro_Subcat = models.ForeignKey(product_subcategory, on_delete=models.CASCADE, default="")
    Pro_image = models.ImageField(upload_to="photos")
    Pro_description = models.TextField()
    Pro_price = models.IntegerField()

    def __str__(self):
        return self.Pro_name

    def Pro_images(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.Pro_image.url))

    Pro_images.allow_tags = True


class product_stock_detail(models.Model):
    Pro_id = models.ForeignKey(product_detail, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Updated_time = models.DateTimeField(auto_now=True, editable=False)

class product_wishlist(models.Model):
    Product_id = models.ForeignKey(product_detail, on_delete=models.CASCADE, default="")
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    Date_time = models.DateTimeField(auto_now=True, editable=False)


class product_cart(models.Model):
    Product_id = models.ForeignKey(product_detail, on_delete=models.CASCADE, default="")
    L_id = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    Product_name = models.CharField(max_length=300)
    Date_time = models.DateTimeField(auto_now=True, editable=False)
    Price = models.IntegerField(default=100)
    Quantity = models.IntegerField()
    Final_price = models.IntegerField()
    Order_id = models.IntegerField(default=0)
    Order_status = models.IntegerField(default=0)


class product_order(models.Model):
    Total_amount = models.IntegerField(default=0)
    L_id = models.ForeignKey(login, on_delete=models.CASCADE)
    Address = models.CharField(max_length=35)
    Order_status = (
        ('pending', 'PENDING'),
        ('placed', 'PLACED'),
    )
    order_status = models.CharField(max_length=50, choices=Order_status)
    Payment_status = models.CharField(max_length=30)
    Date_time = models.DateTimeField(auto_now=True, editable=False)


class feedback(models.Model):
    Name = models.CharField(max_length=50, default="")
    Email = models.EmailField(default="")
    Comment = models.CharField(max_length=250, default="")


class card_detail(models.Model):
    name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=50)
    card_cvv = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=50)
    card_balance = models.IntegerField(default=1000000)

    def __str__(self):
        return self.card_number


class FEEDBACK_TABLE(models.Model):
    L_ID = models.ForeignKey(login, on_delete=models.CASCADE, default="")
    RATINGS = models.CharField(max_length=300)
    COMMENT = models.CharField(max_length=300, default="")

class bottle(models.Model):
    bottle_type = models.CharField(max_length=300)
    bottle_image = models.ImageField(upload_to="photos")

    def __str__(self):
        return self.bottle_type

    def bottle_images(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.bottle_image.url))

    bottle_images.allow_tags = True




class customized(models.Model):
    L_id = models.ForeignKey(login, on_delete=models.CASCADE)
