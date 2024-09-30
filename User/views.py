import openai
from datetime import datetime
import random
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings

from User.models import *
from Admin.models import *
from Guest.models import *


# Create your views here.

def homepage(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/Homepage.html',{'user':user})
   

def myprofile(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/MyProfile.html',{'user':user})
  

def editprofile(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        user.user_name=request.POST.get("txt_name")
        user.user_email=request.POST.get("txt_email")
        user.user_contact=request.POST.get("txt_contact")
        user.user_address=request.POST.get("txt_address")
        user.save()
        return redirect('webuser:myprofile')
    else:
        return render(request,'User/EditProfile.html',{'user':user})
       

  

def changepassword(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        currentpass=request.POST.get("txt_currentpassword")
        if user.user_password == currentpass:
            newpass=request.POST.get("txt_newpassword")
            conpass=request.POST.get("txt_confirmpassword")
            if newpass==conpass:
                user.user_password=newpass
                user.save()
                msg="successfully"
                return render(request,'User/ChangePassword.html',{'msg':msg})
            else:
                msg="Cannot Change Password"
                return render(request,'User/ChangePassword.html',{'msg':msg})
        else:
            msg="Password Incorrect"
            return render(request,'User/ChangePassword.html',{'msg':msg})

    else:
        return render(request,'User/ChangePassword.html')
    

def review(request):
   if request.method=="POST":
      tbl_review.objects.create(review=request.POST.get("txt_review"))
      return redirect("webuser:review")
   else:
      return render(request,'User/Review.html')

def houselist(request):
    # Get the IDs of houses that are either booked or paid (booking_status='1' or payment_status='1')
    booked_or_paid_houses = tbl_booking.objects.filter(
        booking_status='1',
        payment_status='1'
    ).values_list('house_id', flat=True)
    
    # Get the houses that are not booked and not paid for (booking_status='0' and payment_status='0')
    available_houses = tbl_house.objects.exclude(id__in=booked_or_paid_houses)
    
    # Render the available houses to the template
    return render(request, 'User/HouseList.html', {'Data': available_houses})



def search_houses(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        price = request.GET.get('price')
        houses = tbl_house.objects.all()

        if price:
            houses = tbl_house.objects.filter(house_price=price)
        
        house_data = list(houses.values(
            'house_title', 'house_description', 'house_location', 'house_price', 'house_image'
        ))

        # Construct full URL for image field
        for house in house_data:
            house['image_url'] = house['house_image']  # This should be the correct URL

        return JsonResponse({'houses': house_data})
    else:
        houses = tbl_house.objects.all()
     
        context = {
            'Data': houses,
            
        }
        return render(request, 'HouseList.html', context)




def booking(request, did):
    house = tbl_house.objects.get(id=did)  # Get the house instance using did
    user = tbl_user.objects.get(id=request.session['uid'])  # Get the user from session
    
    # Create a new booking
    tbl_booking.objects.create(
        booking_amount=house.house_price,  # Use the house instance's price
        user=user,  # Assign the user instance
        house=house,  # Assign the house instance, not its id
        booking_status=1
    )
    
    return redirect('webuser:mybooking')


def mybooking(request):
    userid=request.session['uid']
    booking=tbl_booking.objects.filter(user=userid)
    return render(request,'User/MyBookings.html',{'Data':booking})

def paymentticket(request,id):
   booking=tbl_booking.objects.get(id=id)
   amount=booking.booking_amount
   if request.method=="POST":
      booking.payment_status=1
      booking.save()
      return redirect("webuser:loader")
   else:
    return render(request,"User/Payment.html",{'amnt':amount})

def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def cancelbooking(request,id):
    booking=tbl_booking.objects.get(id=id)
    booking.status= 3
    booking.save()
    return redirect("webuser:viewmyticket")


def logout(request):
    del request.session["uid"]
    return redirect("webguest:homepage")



# import requests
# from django.http import JsonResponse
# from django.shortcuts import render

# # Replace with your API key
# API_KEY = 'AIzaSyC8b9oHSPOydBF0fRN2nIYipRNDwZG_CCw'
# API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

# # Define predefined responses
# PREDEFINED_RESPONSES = {
#     "Can you tell me what this THRIVEseeds is about?": "Hi, I’m Cropsy! Our e-commerce website THRIVEseeds specializes in selling high-quality crop seeds for various agricultural needs. We offer a wide range of seeds with detailed descriptions, pricing, and weather-based recommendations.",
#     "What kinds of crop seeds do you sell?": "Cropsy here! We offer a diverse range of crop seeds including vegetables, fruits, grains, and pulses. You can browse our categories to find specific types of seeds.",
#     "Can you give me details about a specific seed?": "Sure thing! Just tell me the name or category of the seed you’re interested in, and I’ll provide you with more details.",
#     "How does weather affect the seeds I should buy?": "Great question! Weather plays a crucial role in crop growth. I can help you choose the right seeds based on your local climate conditions using our weather forecasts.",
#     "Can you recommend seeds based on the current weather?": "Absolutely! Based on your location and the current weather conditions, I can suggest the best seeds for optimal growth. Just let me know your location.",
#     "How do I add items to my cart?": "To add items to your cart, simply select the desired seed, choose the quantity, and click the 'Add to Cart' button.",
#     "I want to remove an item from my cart. How do I do that?": "No problem! Go to your cart page, find the item you want to remove, and click the 'Remove' button next to it.",
#     "How do I check out?": "To check out, go to your cart, review the items, and click the 'Proceed to Checkout' button. Follow the prompts to enter your shipping information and payment details.",
#     "I have a problem with my order. Who should I contact?": "If you have any issues with your order, please contact our customer support team through the contact form on our website or by email at deninjose0@gmail.com.",
#     "How can I track my order?": "You can track your order by visiting the 'Order Tracking' section on our website and entering your order number.",
#     "How do I create an account?": "To create an account, click on the 'Sign Up' button on the homepage, fill out the required information, and submit the form. You’ll receive a confirmation email to complete the registration.",
#     "How can I reset my password?": "If you’ve forgotten your password, go to the 'Login' page and click on 'Forgot Password.' Follow the instructions to reset your password.",
#     "What weather conditions should I consider when buying seeds?": "When purchasing seeds, you should consider factors like temperature, humidity, rainfall, and soil conditions. I can provide you with weather forecasts to help you make the right decision.",
#     "Can you give me today’s weather forecast?": "Sure! Let me check the current weather conditions for your location. Could you share your city or town?",
#     "What is the weather forecast for the next 7 days?": "I can provide you with a 7-day weather forecast for your area. Please visit \"weather dashboard\" after login for get weather forecasting data up to 16 days from now.",
#     "How does the weather forecasting feature work?": "THRIVEseeds integrates weather data from reliable sources to help you make informed decisions. The forecasts are updated regularly, and I can provide real-time information for your specific area.",
#     "What are the available payment options?": "We accept major credit cards, debit cards, UPI, and net banking. You can choose your preferred option during checkout.",
#     "How can I contact customer support?": "You can contact our customer support through the contact form on our website or by emailing us at deninjose0@gmail.com.",
#     "What’s your favorite color?": "As much as I’d love to have a favorite color, I’m here to help you with crop seed-related queries! Let me know if you need assistance with any products or weather updates.",
#     "Tell me a joke.": "I’m more of a seed and weather expert, but I can certainly help you grow some great crops! Let me know if you need assistance with anything else.",
#     "How do I fix my car engine?": "I specialize in crop seeds and weather forecasting, so I might not be able to help with that. However, if you have any questions about our products, I’d be happy to assist!",
#     "Can you predict the stock market for me?": "I’m here to provide you with weather forecasts and help with crop seed-related queries. If you’re looking for investment advice, I recommend contacting a financial expert.",
#     "How can I grow flowers in space?": "That’s an exciting question! While I can help you grow crops on Earth, space gardening is a bit out of my expertise. Let me know if you need any tips on planting crops here on Earth.",
#     "Can you recommend seeds based on the current weather?": "Absolutely! To recommend the best seeds for your area, I need to know your location. Please tell me your city or town.",
#     "how are you": "I'm just a chatbot here to assist you with crop seed-related questions. How can I help you today?",
# }



# def chat(request):
#     if request.method == 'POST':
#         user_message = request.POST.get('message')

#         # Retrieve or initialize conversation history
#         conversation_history = request.session.get('conversation_history', [])

#         # Add user message to conversation history
#         conversation_history.append(f"input: {user_message}")

#         # Check if the message matches any predefined response
#         bot_reply = PREDEFINED_RESPONSES.get(user_message, None)
        
#         if not bot_reply:
#             # Define headers and data for the API request
#             headers = {
#                 'Content-Type': 'application/json',
#             }
            
#             # Prepare context: Use the conversation history
#             messages = [{'text': message} for message in conversation_history]
            
#             # Prepare data with context (previous conversation)
#             data = {
#                 'contents': [
#                     {
#                         'parts': messages
#                     }
#                 ]
#             }

#             # Make the API request
#             try:
#                 response = requests.post(f'{API_URL}?key={API_KEY}', headers=headers, json=data)
#                 response.raise_for_status()  # Raise an exception for HTTP errors
                
#                 # Parse the JSON response
#                 api_response = response.json()
#                 print("API Response:", api_response)  # For debugging
                
#                 # Extract the bot reply from the response
#                 bot_reply = api_response['candidates'][0]['content']['parts'][0]['text']
                
#                 # Limit the response to a certain number of sentences (e.g., 3)
#                 bot_reply = '. '.join(bot_reply.split('. ')[:3])  # Limits the response to 3 sentences
                
#             except requests.RequestException as e:
#                 # Handle request errors
#                 print(f"API request error: {e}")
#                 bot_reply = 'Sorry, there was an error processing your request.'

#         # Add bot response to conversation history
#         conversation_history.append(f"output: {bot_reply}")

#         # Store updated conversation history in session
#         request.session['conversation_history'] = conversation_history

#         return JsonResponse({'reply': bot_reply})

#     # Render the chat interface if not a POST request
#     return render(request, 'User/chatbot.html')



# chatbot/views.py


from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

# Configure API key
api_key = "AIzaSyC8b9oHSPOydBF0fRN2nIYipRNDwZG_CCw"
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_text(request):
    if request.method == 'POST':
        user_input = request.POST.get('input_text', '')
        if user_input:
            try:
                # Call generate_content
                response = model.generate_content(user_input)
                # Access the text directly if it's an attribute
                generated_text = response.text if hasattr(response, 'text') else 'No text found'
                return JsonResponse({'generated_text': generated_text})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'No input text provided'}, status=400)
    return render(request, 'User/generate_text.html')







