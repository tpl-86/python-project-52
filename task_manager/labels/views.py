from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Label
from .forms import LabelForm

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = "Метка успешно создана"

class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = "Метка успешно изменена"

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels:label_list')
    success_message = "Метка успешно удалена"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # M2M: запрещаем удалять, если есть связанные задачи
        if self.object.tasks.exists():
            messages.error(request, "Невозможно удалить метку, потому что она используется")
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context, status=200)

        messages.success(request, self.success_message)
        return super().post(request, *args, **kwargs)
