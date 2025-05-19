from django.shortcuts import render, HttpResponse
from home.models import Contact, LostItem, FoundItem
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from home import views
from django.contrib.auth.decorators import login_required
from .models import  UserProfile  # Import the UserProfile model

# Create your views here.
from django.shortcuts import render
from .models import LostItem, FoundItem

def home(request):
    # Count the total number of reports
    total_reports = LostItem.objects.count() + FoundItem.objects.count()

    # Fetch recent lost and found items
    recent_lost_items = LostItem.objects.order_by('-date_lost')[:5]  # Adjust number as needed
    recent_found_items = FoundItem.objects.order_by('-date_found')[:5]  # Adjust number as needed

    # Pass data to the template
    context = {
        'total_reports': total_reports,
        'recent_lost_items': recent_lost_items,
        'recent_found_items': recent_found_items,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, "about.html")

def rfi(request):
    return render(request, "rfi.html")

# def contact(request):
#     if request.method=="POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         desc = request.POST['desc']
#         contact = Contact(fname=fname, lname=lname, email=email, desc=desc)
#         contact.save()
#         print("Written to db")
#         return redirect('success')
#     return render(request, "contact.html")
    

def contact(request):
    if request.method == 'POST':
        # Safely get data from the form
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        email = request.POST.get('email', '')
        desc = request.POST.get('desc', '')

        # Save the message to the database
        contact_message = Contact(fname=fname, lname=lname, email=email, desc=desc)
        contact_message.save()

        # Redirect or show success message
        return render(request, 'success.html')
    

    # Fetch all messages from the Contact model
    messages = Contact.objects.all()

    return render(request, 'contact.html')

def projects(request):
    return render(request, "projects.html")


def success(request):
    return render(request, "success.html")

def success1(request):
    return render(request, "success1.html")

def UserPP(request):
    return render(request, "userpp.html")




# login ko lagi !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       LOGIN!          !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import UserProfile  # Adjust the import according to your project structure

def SignupPage(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        profile_pic = request.FILES.get('profile_pic')  # Handle file input

        # Check if the two passwords match
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already taken, please choose another one.")

        # Create user
        my_user = User.objects.create_user(
            first_name=fname or "N/A",
            last_name=lname or "N/A",  # Default value if last name is not provided
            username=uname,
            email=email,
            password=pass1
        )
        
        # # Check if the UserProfile already exists
        # if not UserProfile.objects.filter(user=my_user).exists():
        #     # Create UserProfile for the user and save profile picture
        #     user_profile = UserProfile(user=my_user, profile_pic=profile_pic)
        #     user_profile.save()
        # else:
        #     return HttpResponse("UserProfile already exists.")

        return redirect('Login Page')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render (request,'doesnot.html')

    return render (request,'login.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")  # Updated to match the field name
        remember = request.POST.get("remember")  # Checkbox value
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Browser session
            return redirect("home")  # Redirect to a home page or dashboard
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

from django.core.mail import send_mail
from django.shortcuts import render

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # Logic to verify email and send a password reset link
        send_mail(
            "Password Reset Request",
            "Click the link below to reset your password.",
            "noreply@yourdomain.com",
            [email],
        )
        return render(request, "forgot_password.html", {"message": "Email sent!"})
    return render(request, "forgot_password.html")

def LogoutPage(request):
    logout(request)
    return redirect('Login Page')

def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        
        if 'profile_pic' in request.FILES:
            user.userprofile.profile_pic = request.FILES['profile_pic']
        
        user.save()
        user.userprofile.save()

        return redirect('home')
    
    return render(request, 'edit_profile.html')

from .forms import LostItemForm

def rli(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        item_name = request.POST.get('item_name')
        item_type = request.POST.get('item_type')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        date_lost = request.POST.get('date_lost')
        location_lost = request.POST.get('location_lost')
        details = request.POST.get('details')
        photo = request.FILES.get('photo')  # Use request.FILES for file uploads

        # Create a new LostItem instance and save it
        lost_item = LostItem(
            name=name,
            email=email,
            phone=phone,
            item_name=item_name,
            item_type=item_type,
            color=color,
            brand=brand,
            date_lost=date_lost,
            location_lost=location_lost,
            details=details,
            photo=photo,
        )
        lost_item.save()  # Save the instance to the database
        print("Written to db")
        return redirect('success')  # Redirect to a success page

    return render(request, "rli.html")  # Render the form on GET request


from .forms import FoundItemForm

def rfi(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        item_name = request.POST.get('item_name')
        item_type = request.POST.get('item_type')
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        date_found = request.POST.get('date_found')
        location_found = request.POST.get('location_found')
        details = request.POST.get('details')
        photo = request.FILES.get('photo')  # Use request.FILES for file uploads

        # Create a new FoundtItem instance and save it
        found_item = FoundItem(
            name=name,
            email=email,
            phone=phone,
            item_name=item_name,
            item_type=item_type,
            color=color,
            brand=brand,
            date_found=date_found,
            location_found=location_found,
            details=details,
            photo=photo,
        )
        found_item.save()  # Save the instance to the database
        print("Written to db")
        return redirect('success')  # Redirect to a success page

    return render(request, "rfi.html")  # Render the form on GET request


from django.shortcuts import render, get_object_or_404, redirect
from .models import LostItem, FoundItem
from .forms import LostItemForm, FoundItemForm  # You’ll need forms to handle editing

def list_reports(request):
    # Retrieve current user's reports
    lost_items = LostItem.objects.filter(email=request.user.email)
    found_items = FoundItem.objects.filter(email=request.user.email)
    
    return render(request, "list_reports.html", {
        "lost_items": lost_items,
        "found_items": found_items,
    })

def edit_report(request, pk, report_type):
    # Determine model based on report type
    model = LostItem if report_type == "lost" else FoundItem
    report = get_object_or_404(model, pk=pk, email=request.user.email)
    
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES, instance=report) if report_type == "lost" else FoundItemForm(request.POST, request.FILES, instance=report)
        
        if form.is_valid():
            form.save()
            return redirect('list_reports')  # Redirect to list after saving

    else:
        form = LostItemForm(instance=report) if report_type == "lost" else FoundItemForm(instance=report)

    return render(request, 'edit_report.html', {
        'form': form,
        'report_type': report_type,
    })

def available_reports(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request

    # Fetch lost and found items based on the search query
    if search_query:
        lost_reports = LostItem.objects.filter(item_name__icontains=search_query)  # Filter lost items
        found_reports = FoundItem.objects.filter(item_name__icontains=search_query)  # Filter found items
    else:
        lost_reports = LostItem.objects.all()  # Fetch all lost items if no query
        found_reports = FoundItem.objects.all()  # Fetch all found items if no query

    context = {
        'lost_reports': lost_reports,
        'found_reports': found_reports,
        'search_query': search_query,  # Pass the search query to the template
    }
    return render(request, 'available_reports.html', context)

def item_detail(request, item_id, model_type):
    if model_type == 'lost':
        item = get_object_or_404(LostItem, id=item_id)
    else:
        item = get_object_or_404(FoundItem, id=item_id)
    return render(request, 'item_detail.html', {'item': item})

def report_view(request):
    search_query = request.GET.get('search', '')

    found_reports = FoundItem.objects.filter(item_name__icontains=search_query)
    lost_reports = LostItem.objects.filter(item_name__icontains=search_query)

    context = {
        'found_reports': found_reports,
        'lost_reports': lost_reports,
        'search_query': search_query,
    }
    return render(request, 'available_reports.html', context)

from django.http import JsonResponse


def get_item_details(request, type, pk):
    if type == 'lost':
        item = LostItem.objects.get(pk=pk)
        data = {
            'item_name': item.item_name,
            'date': item.date_lost.strftime('%B %d, %Y'),
            'details': item.details,
            'location': item.location_lost,
        }
    elif type == 'found':
        item = FoundItem.objects.get(pk=pk)
        data = {
            'item_name': item.item_name,
            'date': item.date_found.strftime('%B %d, %Y'),
            'details': item.details,
            'location': item.location_found,
        }
    else:
        return JsonResponse({'error': 'Invalid type'}, status=400)
    return JsonResponse(data)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import LostItem, FoundItem, Claim
from django.core.mail import send_mail

def claim_item(request, model_name, item_id):
    # Fetch the item based on the model_name
    if model_name == 'lost':
        item = get_object_or_404(LostItem, id=item_id)
    elif model_name == 'found':
        item = get_object_or_404(FoundItem, id=item_id)
    else:
        messages.error(request, "Invalid model type.")
        return redirect('available_reports')

    if request.method == 'POST':
        # Retrieve form data
        claimant_name = request.POST.get('name')
        claimant_email = request.POST.get('email')
        claimant_phone = request.POST.get('phone')
        claim_message = request.POST.get('message')

        # Save the claim to the database
        claim = Claim(
            item=item if model_name == 'lost' else None,
            found_item=item if model_name == 'found' else None,
            claimant_name=claimant_name,
            claimant_email=claimant_email,
            claimant_phone=claimant_phone,
            claim_message=claim_message
        )
        claim.save()
        # # Send email to the claimant
        # subject_to_claimant = 'Successfully Claimed'
        # message_to_claimant = 'The item is claimed successfully. Thank you for using our platform.'
        # send_mail(
        #     subject_to_claimant,
        #     message_to_claimant,
        #     'your_email@example.com',  # Replace with your sender email
        #     [claimant_email],
        # )

        # # Send email to the item's owner
        # item_owner_email = item.owner.email  # Assuming the item model has an 'owner' field with an email
        # subject_to_owner = f"Your item '{item.name}' has been claimed"
        # message_to_owner = (
        #     f"Hello {item.owner.name},\n\n"
        #     f"Your item '{item.name}' has been claimed by {claimant_name}.\n"
        #     f"Contact details:\n"
        #     f"Name: {claimant_name}\n"
        #     f"Email: {claimant_email}\n"
        #     f"Phone: {claimant_phone}\n\n"
        #     f"Message from claimant:\n{claim_message}\n\n"
        #     f"Thank you for using our platform."
        # )
        # send_mail(
        #     subject_to_owner,
        #     message_to_owner,
        #     'shronalduwal999@gmail.com',  # Replace with your sender email
        #     [item_owner_email],
        # )

        # Redirect to a success page
        messages.success(request, "Claim submitted successfully. Notifications have been sent.")
        return redirect('success1')
        # Display a success message
        return redirect('available_reports')

    return render(request, 'claim_form.html', {'item': item, 'model_name': model_name})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_item_details(request, item_type, item_id):
    if item_type == 'found':
        item = get_object_or_404(FoundItem, id=item_id)
    elif item_type == 'lost':
        item = get_object_or_404(LostItem, id=item_id)
    else:
        return JsonResponse({'error': 'Invalid item type'}, status=400)

    data = {
        'id': item.id,
        'item_name': item.item_name,
        'location': item.location_found if item_type == 'found' else item.location_lost,
        'date': item.date_found if item_type == 'found' else item.date_lost,
        'name': item.name,
        'photo': item.photo.url if item.photo else None,
    }
    return JsonResponse(data)



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # This saves the new password to the database
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Redirect to a profile or success page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

from django.contrib.auth.hashers import make_password

def set_new_password(user, raw_password):
    user.password = make_password(raw_password)
    user.save()
