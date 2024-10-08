from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
from decouple import config
# Create your views here.


def contact(request):
    myEmail = config('MY_EMAIL')
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(
                    request, 'You have already made inquiry for this listing')
                return redirect('/listings/'+listing_id)
        contact = Contact(listing=listing, listing_id=listing_id, name=name,
                          email=email, phone=phone, message=message, user_id=user_id)
        contact.save()
        send_mail(
            "Property Listing Inquiry",  # subject
            "There has been an inquiry for " + listing + \
            ". Sign into the admin panel for more info",
            myEmail,  # from email
            [myEmail, 'u0g6d@yahoo.com.hk', 'hcpoon@simitrigroup.com'],
            fail_silently=False,
        )
        messages.success(
            request, 'You request has been submitted, a realtor will get back to you soon')
    return redirect('/listings/'+listing_id)
