from django.views import generic
from map.forms import PointForm
# from apps.users.forms import


class MapPageView(generic.TemplateView):
    template_name = "map/map_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_point_form"] = PointForm
        return context


class MainPageView(generic.TemplateView):
    template_name = "map/main_page.html"


# class UserSignUpView(generic.CreateView):
#     template_name = "users/sign_up.html"
#     form_class =


