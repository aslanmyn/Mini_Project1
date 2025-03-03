from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from products.models import Product
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import UserSerializer
from .permissions import IsAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from trading.models import TradeRequest

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    

def homepage(request):
    return render(request, 'homepage/home.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        username = request.POST.get('userName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'users/register.html')

        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            phone_number=phone_number,
            address=address,
        )
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        messages.success(request, 'Account created successfully! Log In now!')
        return redirect('login')
    return render(request, 'users/register.html')


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        context["products"] = Product.objects.filter(representative=profile_user)  # Get only this user's products
        context["received_trade_requests"] = TradeRequest.objects.filter(trader=profile_user, status='pending')
        context["sent_trade_requests"] = TradeRequest.objects.filter(customer=profile_user)
        return context


    
    
    
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    context_object_name = 'profile_user'
    template_name = 'users/profile_update.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def test_func(self):
        return self.get_object() == self.request.user  # Only allow the user to edit their own profile

    def form_valid(self, form):
        user = form.save(commit=False)  # Save form but don't commit to DB yet
        user.profile_picture = self.request.FILES.get('image', user.profile_picture)  # Profile image
        user.address = self.request.POST.get('address', user.address)  # Address
        user.phone_number = self.request.POST.get('phone_number', user.phone_number)
        user.first_name = self.request.POST.get('first_name', user.first_name)# Phone
        user.save()  # Save to database
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
    
    

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/profile_delete.html'
    context_object_name = 'profile_user'
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def test_func(self):
        return self.get_object() == self.request.user  # Only allow the user to delete their own profile
    
    

    




