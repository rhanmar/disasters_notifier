from django.views import generic
from map.forms import PointForm


class MapPageView(generic.TemplateView):
    template_name = "map/map_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_point_form"] = PointForm
        return context


class MainPageView(generic.TemplateView):
    template_name = "map/main_page.html"




