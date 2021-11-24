from django.views import generic
from map.forms import PointForm, PointAdminForm, PointUserOwnerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class MapPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "map/map_page.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_point_form"] = PointForm
        context["point_form_admin"] = PointAdminForm
        context["point_form_owner"] = PointUserOwnerForm
        return context


class MainPageView(LoginRequiredMixin, generic.TemplateView):
    template_name = "map/main_page.html"  # TODO move templates dir
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        print(self.request.user)
        print(self.request.user.is_authenticated)
        return super().get_context_data(**kwargs)
