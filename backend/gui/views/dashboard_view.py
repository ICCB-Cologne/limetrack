from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse)
from django.views.generic import TemplateView
from django.shortcuts import render
from ..models import HistopathologicalSample
from typing import Any
import plotly.graph_objects as go


class DashboardView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/dashboard.html"
        samples = HistopathologicalSample.objects.all()

        get_dict = request.GET
        print(get_dict)

        if get_dict.get("count_what"):
            count_this = get_dict["count_what"]
        else:
            count_this = "recruiting_site"

        real_sites = [
            [getattr(instance, field.name)
                for field in instance._meta.fields
                if field.name == count_this]
            for instance in samples
        ]
        keys = [site[0] for site in real_sites]
        keys = list(set(keys))
        d = dict()
        for key in keys:
            d.update({key: 0})
        for site in real_sites:
            d[site[0]] += 1

        fig1 = go.Figure(data=[go.Bar(x=list(d.keys()), y=list(d.values()),
                                      marker_color="rgba(25,42,98,255)")])

        fig2 = go.Figure(data=[go.Bar(x=list(d.keys()), y=list(d.values()),
                                      marker_color="rgba(150,77,0,255)")])

        plot1 = fig1.to_html(full_html=False)
        plot2 = fig2.to_html(full_html=False)

        context = {
            "samples": real_sites,
            "plot1": plot1,
            "plot2": plot2,
            "user": request.user  # user, not username because we
                                  # need to check the user's attributes
        }
        return render(request, template_name, context=context)
