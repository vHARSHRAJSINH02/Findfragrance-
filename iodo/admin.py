from django.contrib import admin
from .models import login
from .models import customer_detail
from .models import area
from .models import city
from .models import state
from .models import product_category
from .models import product_subcategory
from .models import product_detail
from .models import product_stock_detail
from .models import product_order
from .models import feedback
from .models import product_cart
from .models import card_detail
from .models import FEEDBACK_TABLE
from .models import product_wishlist
# Register your models here.
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 14),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.beige),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ['L_id', 'Total_amount', 'Payment_status','Date_time','Address']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.L_id, obj.Total_amount, obj.Payment_status,obj.Date_time,obj.Address])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"




class Login(admin.ModelAdmin):
    list_display = ["Email","Password","Phone","Role","Status"]
admin.site.register(login,Login)

class Customer_Detail(admin.ModelAdmin):
    list_display = ["Name","L_id","Dob","Address","customer_photos","Area_id","City","State_id"] #
admin.site.register(customer_detail,Customer_Detail)

class Area(admin.ModelAdmin):
    list_display = ["Area_name","City_id","STATE"]
admin.site.register(area,Area)

class City(admin.ModelAdmin):
    list_display = ["City_name","State_id"]
admin.site.register(city,City)


class State(admin.ModelAdmin):
    list_display = ["State_name"]
admin.site.register(state,State)

class Product_Category(admin.ModelAdmin):
    list_display = ["id","Product_category_name"]
admin.site.register(product_category,Product_Category)

class Product_Subcategory(admin.ModelAdmin):
    list_display = ["id","Product_subcategory_name","Product_cat"]
admin.site.register(product_subcategory,Product_Subcategory)

class Product_Detail(admin.ModelAdmin):
    list_display = ["Pro_name","Pro_images","Pro_Cat","Pro_description","Pro_price"]
admin.site.register(product_detail,Product_Detail)

class Product_Stock_Detail(admin.ModelAdmin):
    list_display = ["Pro_id","Quantity","Updated_time"]
admin.site.register(product_stock_detail,Product_Stock_Detail)

class Product_Wishlist(admin.ModelAdmin):
    list_display = ["Product_id","L_id","Date_time"]
admin.site.register(product_wishlist,Product_Wishlist)

class Product_Cart(admin.ModelAdmin):
    list_display = ["Product_id","L_id","Product_name","Date_time","Price","Quantity","Final_price","Order_id","Order_status"]
admin.site.register(product_cart,Product_Cart)


class Product_Order(admin.ModelAdmin):
    list_display = ["Total_amount","L_id","Address","order_status","Payment_status","Date_time"]
    list_filter = ['Date_time']
    actions = [export_to_pdf]


admin.site.register(product_order,Product_Order)

class Feedback(admin.ModelAdmin):
    list_display = ["Name","Email","Comment"]
admin.site.register(feedback,Feedback)

class Card_Detail(admin.ModelAdmin):
    list_display = ["name","card_number","card_cvv","exp_date","card_balance"]
admin.site.register(card_detail,Card_Detail)

class Feedback_Table(admin.ModelAdmin):
    list_display = ["L_ID","RATINGS","COMMENT"]
admin.site.register(FEEDBACK_TABLE,Feedback_Table)