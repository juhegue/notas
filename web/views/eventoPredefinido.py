# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from web.models import AgendaEventoPredefinido, AgendaEventoColor
from web.forms.eventoPredefinidoForm import EventoPedefinidoForm


def get_color(request, color):
    if color.startswith('#'):
        color = color.upper()
        qcolor = AgendaEventoColor.objects.filter(usuario=request.user, color=color).first()
    else:
        qcolor = AgendaEventoColor.objects.filter(pk=color).first()

    if not qcolor:
        qcolor = AgendaEventoColor()
        qcolor.usuario = request.user
        qcolor.color = color
        qcolor.save()
    return qcolor


class RequiredEventoMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            pre = get_object_or_404(AgendaEventoPredefinido, pk=kwargs.get('pk'))
            if pre.usuario != request.user:
                messages.error(request, _('Sin permisos para esta acción.'))
                return redirect('logout_portal')
        return super().dispatch(request, *args, **kwargs)


class EventoPredefinidoListView(LoginRequiredMixin, ListView):
    model = AgendaEventoPredefinido
    template_name = 'web/predefinido/lista.html'

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hidden"] = True
        return context


class EventoPredefinidoCreateView(LoginRequiredMixin, CreateView):
    model = AgendaEventoPredefinido
    template_name = 'web/predefinido/editar.html'
    form_class = EventoPedefinidoForm
    success_url = reverse_lazy('evento_predefinido_lista')
    success_message = _('Evento predefinido creado.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_view"] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = None
        return kwargs

    def form_valid(self, form):
        f = form.save(commit=False)
        data = form.cleaned_data
        color = data.get('color')
        dias = data.get('dias') or 0
        horas = data.get('horas') or 0
        minutos = data.get('minutos') or 0

        f.color = get_color(self.request, color)
        f.usuario = self.request.user
        f.duracion = dias * 24 * 60 + horas * 60 + minutos
        f.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class EventoPredefinidoUpdateView(RequiredEventoMixin, UpdateView):
    model = AgendaEventoPredefinido
    template_name = 'web/predefinido/editar.html'
    form_class = EventoPedefinidoForm
    success_url = reverse_lazy('evento_predefinido_lista')
    success_message = _('Evento predefinido modificado.')

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user)
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['object'] = self.object
        return kwargs

    def form_valid(self, form):
        f = form.save(commit=False)
        data = form.cleaned_data
        color = data.get('color')
        dias = data.get('dias') or 0
        horas = data.get('horas') or 0
        minutos = data.get('minutos') or 0

        f.color = get_color(self.request, color)
        f.duracion = dias * 24 * 60 + horas * 60 + minutos
        f.save()
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class EventoPredefinidoDeleteView(RequiredEventoMixin, DeleteView):
    model = AgendaEventoPredefinido
    template_name = 'web/predefinido/eliminar.html'
    success_message = _('Evento prefefinido eliminado.')

    def get_queryset(self):
        queryset = AgendaEventoPredefinido.objects.filter(usuario=self.request.user)
        return queryset

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('evento_predefinido_lista')
