from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()

    # check to see if user is logging in

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error Logging you in, Please Try Again...")
            return redirect('home')
        
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            # authenticate and log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have Successfully Registered! Welcome...")
            return redirect('home')
        
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:

        customer_record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    
    else:
        messages.success(request, "You are not authorized to view records!")
        return redirect('home')
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        to_delete = Record.objects.get(id = pk)
        to_delete.delete()

        messages.success(request, "Record have been Deleted Successfully!")

    else:
        messages.success(request, "You are not authorized to Delete the Record!")
    return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully!")
                return redirect('home')
            
        return render(request, 'add_record.html', {'form': form})

    messages.success(request, "You must be Logged In to Add a Record!")
    return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)

        form = AddRecordForm(request.POST or None, instance=current_record)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Updated Successfully!")
                return redirect('home')
        
        return render(request, 'update_record.html', {'form': form})
    
    else:
        return redirect('home')

    