from django.shortcuts import render,redirect
import openai
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from Admin.models import *
from Guest.models import *
from User.models import *

# Create your views here.
def home_page(request):
    return render(request,'Admin/Homepage.html')

def add_house(request):
    Cdata=tbl_category.objects.all()
    Hdata=tbl_house.objects.all()
    if request.method=="POST" and request.FILES:
     
     
     title=request.POST.get("txt_title")
     description=request.POST.get("txt_description")
     price=request.POST.get("txt_price")
     image=request.FILES.get("txt_image")
     category=tbl_category.objects.get(id=request.POST.get("select"))
     location=request.POST.get("txt_location")
     tbl_house.objects.create(house_title=title,house_description=description,house_category=category,house_image=image,house_price=price,house_location=location,admin=tbl_admin.objects.get(id=request.session["aid"]))
     return render(request,'Admin/AddHouse.html',{'Data':Cdata,'HouseData':Hdata})
    else:
       return render(request,'Admin/AddHouse.html',{'Data':Cdata,'HouseData':Hdata})

def add_houselist(request):
   Data=tbl_house.objects.all()
   return render(request,'Admin/AddHouseList.html',{'HouseData':Data})     
       
def category(request):
    Cdata=tbl_category.objects.all()
    if request.method=="POST":
       name=request.POST.get("txt_name")
       tbl_category.objects.create(category_name=name)
       return render(request,'Admin/Category.html',{'Data':Cdata})
    else:
        return render(request,'Admin/Category.html',{'Data':Cdata})

def categorylist(request):
   Cdata=tbl_category.objects.all()
   return render(request,'Admin/CategoryList.html',{'Data':Cdata})
      
       
def update_category(request,did):
   Cdata=tbl_category.objects.all()
   updata=tbl_category.objects.get(id=did)
   if request.method=="POST":
        name=request.POST.get("txt_name")
        updata.category_name=name
        updata.save()
        return redirect('webadmin:Category')
   else:
      return render(request,'Admin/Category.html',{'Data':Cdata,'udata':updata})
      
      
def delete_category(request,did):
   tbl_category.objects.get(id=did).delete()
   return redirect('webadmin:Category')

def update_house(request,did):
   Cdata=tbl_category.objects.all()
   Hdata=tbl_house.objects.all()
   updata=tbl_house.objects.get(id=did)
   if request.method=="POST":
     title=request.POST.get("txt_title")
     description=request.POST.get("txt_description")
     price=request.POST.get("txt_price")
     image=request.FILES.get("txt_image")
     category=tbl_category.objects.get(id=request.POST.get("select"))
     location=request.POST.get("txt_location")
     updata.house_title=title
     updata.house_description=description
     updata.house_price=price
     updata.house_image=image
     updata.house_category=category
     updata.house_location=location
     updata.save()
     return redirect('webadmin:add_house')
   else:
     return render(request,'Admin/AddHouse.html',{'udata':updata,'Data':Cdata,'Hdata':Hdata})
      

def delete_house(request,did):
   tbl_house.objects.get(id=did).delete()
   return redirect('webadmin:add_house')

def report(request):
    booking = tbl_booking.objects.all()
    return render(request,'Admin/Report.html',{"booking":booking})



def ajaxreport(request):
    if (request.GET.get("fdate")!="") and (request.GET.get("tdate")!="") and (request.GET.get("status")!=""):
        booking = tbl_booking.objects.filter(date__gte=request.GET.get("fdate"),date__lte=request.GET.get("tdate"),status=request.GET.get("status"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})
    elif (request.GET.get("fdate")!="") and (request.GET.get("status")!=""):
        booking = tbl_booking.objects.filter(date__gte=request.GET.get("fdate"),status=request.GET.get("status"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})
    elif (request.GET.get("tdate")!="") and (request.GET.get("status")!=""):
        booking = tbl_booking.objects.filter(date__lte=request.GET.get("tdate"),status=request.GET.get("status"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})
    elif request.GET.get("fdate")!="":
        booking = tbl_booking.objects.filter(date__gte=request.GET.get("fdate"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})
    elif request.GET.get("tdate")!="":
        booking = tbl_booking.objects.filter(date__lte=request.GET.get("tdate"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})
    elif request.GET.get("status")!="":
        booking = tbl_booking.objects.filter(status=request.GET.get("status"))
        return render(request,"Admin/AjaxReport.html",{"booking":booking})


def logout(request):
    del request.session["aid"]
    return redirect("webguest:homepage")


def ownerslist(request):
    # Fetch houses along with their related owners using select_related
    houses = tbl_house.objects.select_related('owner').all()
    owner_data = {}
    ownerless_houses = []  # Separate list for houses without an owner

    for house in houses:
        owner = house.owner
        if owner:  # Check if owner is not None
            if owner.id not in owner_data:
                owner_data[owner.id] = {
                    'name': owner.owner_name,
                    'contact': owner.owner_contact,
                    'email': owner.owner_email,
                    'gender': owner.owner_gender,
                    'address': owner.owner_address,
                    'houses': []
                }
            
            owner_data[owner.id]['houses'].append({
                'house_title': house.house_title,
                'house_description': house.house_description,
                'house_price': house.house_price
            })
        else:
            # Add houses with no owner to the ownerless_houses list
            ownerless_houses.append({
                'house_title': house.house_title,
                'house_description': house.house_description,
                'house_price': house.house_price,
                'owner': "No Owner",
                'contact': "N/A",
                'email': "N/A",
                'gender': "N/A",
                'address': "N/A"
            })

    # If any owner has no house, ensure they are added as well (Optional)
    owners_without_houses = tbl_owner.objects.exclude(id__in=owner_data.keys())
    for owner in owners_without_houses:
        owner_data[owner.id] = {
            'name': owner.owner_name,
            'contact': owner.owner_contact,
            'email': owner.owner_email,
            'gender': owner.owner_gender,
            'address': owner.owner_address,
            'houses': [{
                'house_title': "No House Registered",
                'house_description': "No House Registered",
                'house_price': "No House Registered"
            }]
        }

    # Pass both owner data and ownerless houses to the template
    return render(request, 'Admin/ownerslist.html', {
        'owners': owner_data.values(),
        'ownerless_houses': ownerless_houses
    })







# Initialize OpenAI with the API key
# openai.api_key = settings.OPENAI_API_KEY

def send_booking_mail(request, booking_id):
    # Get the booking object
    booking = get_object_or_404(tbl_booking, id=booking_id)
    user_email = booking.user.user_email  # Get the user's email from the booking relationship

    # Create a prompt to generate the email content dynamically using AI
    prompt = f'''
    You are an assistant. Write an email to a user about their house booking.
    Here are the details:
    - User name: {booking.user.user_name}
    - House: {booking.house.house_title}
    - Booking Date: {booking.booking_date}
    - Booking Amount: {booking.booking_amount}
    - Status: {'Paid' if booking.payment_status == '1' else 'Not Paid'}

    The email should be friendly and professional.
    '''

    try:
        # Generate the email content using OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )

        # Extract the AI-generated email content
        generated_email = response.choices[0].text.strip()

        # Send the email using Django's email functionality
        subject = f"Booking Report for {booking.house.house_title}"
        from_email = 'your_email@example.com'  # Replace with your sender email
        recipient_list = [user_email]

        # Send the email
        send_mail(subject, generated_email, from_email, recipient_list)
        
        # Inform the user that the email was sent successfully
        messages.success(request, 'Email sent successfully with AI-generated content!')
    
    except Exception as e:
        # Handle any errors that occur during the email process
        messages.error(request, f"Failed to send email: {e}")

    return redirect('webadmin:report')  # Redirect to the report page after sending


