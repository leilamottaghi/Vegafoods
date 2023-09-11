from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserProfileForm ,UserAddressForm
from .models import UserProfile,UserAddressModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm





class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)        
            
            return redirect('accounts:profile') 
            
        return render(request, 'accounts/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:shop')  
        return render(request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('shop:shop') 



class EditUserProfileView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, 'accounts/editprofile.html', {'form': form})

    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('shop:shop')  

        return render(request, 'accounts/editprofile.html', {'form': form})



class EditUserAddressView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request, address_id):
        user_address = UserAddressModel.objects.get(id=address_id)

        if user_address.user != request.user:
            return HttpResponseForbidden("شما اجازه دسترسی به این آدرس را ندارید.")

        form = UserAddressForm(instance=user_address)
        return render(request, 'accounts/edit_address.html', {'form': form, 'user_address': user_address})

    def post(self, request, address_id):
        user_address = UserAddressModel.objects.get(id=address_id)

        if user_address.user != request.user:
            return HttpResponseForbidden("شما اجازه دسترسی به این آدرس را ندارید.")

        form = UserAddressForm(request.POST, instance=user_address)
        if form.is_valid():
            form.save()
            return redirect('shop:shop') 
        return render(request, 'accounts/edit_address.html', {'form': form, 'user_address': user_address})




class CreateAddressView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserAddressForm()
        return render(request, 'accounts/create_address.html', {'form': form})

    def post(self, request):
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user_address = form.save(commit=False)
            user_address.user = request.user
            user_address.save()
            return redirect('accounts:profile')  

        return render(request, 'accounts/create_address.html', {'form': form})



class UserProfileView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        print("user_profile",user_profile)

        orders ="orders"
        
        invoices = "invoices"
        
        user_addresses = UserAddressModel.objects.filter(user=request.user).order_by('-date_created')
        
        return render(request, 'accounts/profile.html', {
            'user_profile': user_profile,
            'orders': orders,
            'invoices': invoices,
            'user_addresses': user_addresses,
        })


