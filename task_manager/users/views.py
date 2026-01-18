from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.db.models.deletion import ProtectedError


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    queryset = User.objects.order_by('id')


class SelfOnlyMixin(LoginRequiredMixin):
    """Разрешаем изменять/удалять только самого себя.
    Проверяем pk из URL до любых действий, чтобы не дать попасть в form_valid/delete.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        target_pk = kwargs.get('pk')
        if target_pk is not None and int(target_pk) != request.user.pk:
            messages.error(request, 'Вы не можете изменять или удалять другого пользователя')
            return redirect('users:list')
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return response


class UserUpdateView(SelfOnlyMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)


class UserDeleteView(SelfOnlyMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')

    def post(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'Пользователь успешно удалён')
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Пользователя нельзя удалить, потому что он связан с задачами')
            return self.get(request, *args, **kwargs)


class CustomLoginView(BaseLoginView):
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Вы разлогинены')
    return redirect(reverse_lazy('home'))