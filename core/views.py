from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import requests
import json

from .models import Partner, Testimonial, PartnershipApplication, Program, Branch, ProgramRegistration, ContactMessage, CareerApplication
from .forms import PartnershipForm


def index(request):
    """Render the main index page from templates/index.html."""
    partners = Partner.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    programs = Program.objects.filter(is_active=True)[:3]
    context = {
        "partners": partners,
        "testimonials": testimonials,
        "programs": programs,
    }
    return render(request, "index.html", context)


def about(request):
    """Render the About Us page from templates/about.html."""
    return render(request, "about.html")


def partnership(request):
    """Render the Partnership page and handle form submission."""
    if request.method == 'POST':
        form = PartnershipForm(request.POST)
        if form.is_valid():
            application = PartnershipApplication.objects.create(
                school_name=form.cleaned_data['school_name'],
                school_address=form.cleaned_data['school_address'],
                school_phone=form.cleaned_data['school_phone'],
                school_email=form.cleaned_data['school_email'],
                class_type=form.cleaned_data['class_type']
            )
            
            # Send email notification
            subject = f'New Partnership Application - {application.school_name}'
            message = f"""
            New Partnership Application Received
            
            School Name: {application.school_name}
            School Address: {application.school_address}
            School Phone: {application.school_phone}
            School Email: {application.school_email}
            Class Type: {application.get_class_type_display()}
            
            Please review this application in the admin panel.
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            
            messages.success(request, 'Thank you for your partnership request! We will contact you soon.')
            form = PartnershipForm()  # Reset form
    else:
        form = PartnershipForm()
    
    return render(request, "partnership.html", {'form': form})


def programs(request):
    """List all active programs."""
    programs = Program.objects.filter(is_active=True)
    return render(request, "programs.html", {'programs': programs})


def program_register(request, program_id):
    """Handle program registration."""
    program = Program.objects.get(id=program_id, is_active=True)
    branches = Branch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        mode = request.POST.get('mode')
        duration = request.POST.get('duration')
        participants = int(request.POST.get('participants', 1))
        
        if mode == 'online' and duration == '6weeks':
            price_per_person = program.price_online_6weeks
        elif mode == 'online' and duration == '12weeks':
            price_per_person = program.price_online_12weeks
        elif mode == 'offline' and duration == '6weeks':
            price_per_person = program.price_offline_6weeks
        else:
            price_per_person = program.price_offline_12weeks
        
        total_price = price_per_person * participants
        
        registration = ProgramRegistration.objects.create(
            program=program,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            mode=mode,
            branch_id=request.POST.get('branch') if mode == 'offline' else None,
            duration=duration,
            participants=participants,
            total_price=total_price
        )
        
        # Store registration ID in session for payment verification
        request.session['registration_id'] = registration.id
        
        return JsonResponse({
            'registration_id': registration.id,
            'email': registration.email,
            'amount': int(total_price * 100)  # Paystack expects amount in kobo
        })
    
    return render(request, "program_register.html", {
        'program': program,
        'branches': branches,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    })


@csrf_exempt
def verify_payment(request):
    """Verify Paystack payment."""
    if request.method == 'POST':
        data = json.loads(request.body)
        reference = data.get('reference')
        
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers
        )
        
        result = response.json()
        
        if result['status'] and result['data']['status'] == 'success':
            registration_id = request.session.get('registration_id')
            if registration_id:
                registration = ProgramRegistration.objects.get(id=registration_id)
                registration.payment_reference = reference
                registration.payment_status = 'success'
                registration.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment verified successfully!'
                })
        
        return JsonResponse({
            'status': 'failed',
            'message': 'Payment verification failed'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def contact(request):
    """Handle contact form."""
    if request.method == 'POST':
        contact_msg = ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        
        # Send email notification
        email_subject = f'New Contact Message - {contact_msg.subject}'
        email_message = f"""
        New Contact Message Received
        
        Name: {contact_msg.name}
        Email: {contact_msg.email}
        Phone: {contact_msg.phone}
        Subject: {contact_msg.subject}
        
        Message:
        {contact_msg.message}
        
        Please respond to this inquiry.
        """
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
    
    return render(request, "contact.html")


def careers(request):
    """Handle career applications."""
    if request.method == 'POST':
        CareerApplication.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            position=request.POST.get('position'),
            cv=request.FILES.get('cv'),
            passport=request.FILES.get('passport'),
            application_letter=request.POST.get('application_letter')
        )
        messages.success(request, 'Your application has been submitted successfully!')
    
    return render(request, "careers.html")


def handler404(request, exception):
    """Custom 404 error handler."""
    return render(request, '404.html', status=404)


def handler500(request):
    """Custom 500 error handler."""
    return render(request, '500.html', status=500)
