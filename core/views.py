from django.shortcuts import render,redirect
from core.models import MenuItem, Order
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from core.models import UserData
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def home(request):
    return render(request, 'core/home.html')  
  
@login_required(login_url='login')
def menu(request):
    querryset = MenuItem.objects.all()
    user_data = None
    if request.user.is_authenticated:
        try:
            user_data = UserData.objects.get(user=request.user)
        except UserData.DoesNotExist:
            user_data = None
    context = {
        'menu_items': querryset,
        'user_data': user_data,
    }
    return render(request, 'core/menu.html',context)

@login_required(login_url='login')
def menu_detail(request, id):
    menu_item = MenuItem.objects.get(id=id)
    return render(request, 'core/viewmenu.html', {'menu_item': menu_item})

def login_page(request):
    
    if request.user.is_authenticated:
        return redirect("menu")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if not User.objects.filter(username=username).exists():
            return render(request, 'core/login.html', {"error": "Invalid Username!"})
        
        if user is not None:
            login(request, user)
            return redirect("menu")
        else:
            return render(request, 'core/login.html', {"error": "Invalid username or password."})
    return render(request, 'core/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        profile_picture = request.FILES.get("profile_picture")

        if User.objects.filter(username=username).exists():
            return render(request, "core/register.html", {"error": "Username already exists."})
        if User.objects.filter(email=email).exists():
            return render(request, "core/register.html", {"error": "Email already exists."})

        with transaction.atomic():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            userdata = UserData.objects.create(
                user=user,
                address=address,
                phone=phone,
                profile_picture=profile_picture
            )
        return redirect("login")
    return render(request, "core/register.html")

def logout_view(request):
    logout(request)
    return redirect("login")
    

@login_required(login_url='login')
def order_confirm(request, id):
    menu_item = MenuItem.objects.get(id=id)
    user_data = UserData.objects.get(user=request.user)
    if request.method == "POST":
        order_type = request.POST.get("order_type", "online")
        order_number = str(random.randint(10000, 99999))
        order = Order.objects.create(
            user=request.user,
            menu_item=menu_item,
            order_number=order_number,
            order_type=order_type
        )
        # Email sending (template and password to be filled by you)
       
        email_html = render_to_string('core/email_template.html', {
            'order': order,
            'user_data': user_data,
            'menu_item': menu_item,
        })
        send_mail(
            subject=f"Order Confirmation #{order_number}",
            message="",
            from_email=settings.EMAIL_HOST_USER,  # Use the configured sender
            recipient_list=[request.user.email],
            html_message=email_html,
            fail_silently=True,
        )
        return redirect('invoice', order_number=order_number)
    return redirect('menu_detail', id=id)

@login_required(login_url='login')
def invoice(request, order_number):
    order = Order.objects.get(order_number=order_number)
    menu_item = order.menu_item
    user_data = UserData.objects.get(user=order.user)
    return render(request, 'core/invoice.html', {
        'order': order,
        'menu_item': menu_item,
        'user_data': user_data,
    })
    
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order.html', {'orders': orders})

def chefs(request):
    return render(request,'core/chef.html')

def about(request):
    return render(request, 'core/about.html')