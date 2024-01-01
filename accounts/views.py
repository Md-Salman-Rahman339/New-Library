from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from books.models import Book,BorrowedBook


class UserRegistrationView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) 
    

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        user_bought_books = BorrowedBook.objects.filter(user=request.user)
        return render(request, self.template_name, {'form': form, 'data': user_bought_books})
    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        user_bought_books = BorrowedBook.objects.filter(user=request.user)  
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form, 'data': user_bought_books})

    
    