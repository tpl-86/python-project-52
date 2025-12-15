from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    queryset = User.objects.order_by('id')


class OnlySelfAccessMixin(LoginRequiredMixin):
    def dispath(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, 'Вы не можете изменять или удалять другого пользователя.')
            return redirect('users:list')
        return super().dispatch(request, *args, *kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return response


class UserUpdateView(OnlySelfAccessMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(OnlySelfAccessMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Пользователь успешно удален')
        return super().post(request, *args, **kwargs)
