from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="main")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо " + username + "! Ваш обліковий запис успішно створено!")
            return redirect(to="main")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="main")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"З поверненням, {user.username}!")
            return redirect(to="main")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "До побачення! Будемо раді Вас побачити знов!")
        return redirect(to="main")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    try:
        template_name = 'accounts/password_reset.html'
        email_template_name = 'accounts/password_reset_email.html'
        html_email_template_name = 'accounts/password_reset_email.html'
        success_url = reverse_lazy('accounts:password_reset_done')
        subject_template_name = 'accounts/password_reset_subject.txt'
    except Exception as e:
        print(f"Error sending email: {e}")
