from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse)
from django.views.generic import TemplateView
from django.shortcuts import render
from ..models import HistopathologicalSample
from typing import Any
import plotly.graph_objects as go


def count_samples_by_category(samples: list[HistopathologicalSample]):
    plot_dicts = []

    count_by = ["recruiting_site", "saturn3_sample_code"]

    for c in count_by:
        key_value_pairs = [
            [getattr(instance, field.name)
                for field in instance._meta.fields
                if field.name == c]
            for instance in samples
        ]
        keys = [site[0] for site in key_value_pairs]
        keys = list(set(keys))
        counter_dict = dict()

        for key in keys:
            if c == "saturn3_sample_code":
                # count entities (S3C, S3P, S3M)
                key = key[:3]
            counter_dict.update({key: 0})

        for key_value in key_value_pairs:
            if c == "saturn3_sample_code":
                counter_dict[key_value[0][:3]] += 1
            else:
                counter_dict[key_value[0]] += 1
        plot_dicts.append(counter_dict)


class DashboardView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/dashboard.html"
        samples = HistopathologicalSample.objects.all()

        # get_dict = request.GET

        # if get_dict.get("count_what"):
        #     count_this = get_dict["count_what"]
        # else:
        #     count_this = "recruiting_site"

        plot_dict = count_samples_by_category(samples)

        figure_dict = {}
        index = 1
        for dic in plot_dict:

            fig = go.Figure(
                data=[go.Bar(x=list(dic.keys()), y=list(dic.values()),
                             marker_color="rgba(25,42,98,255)")])

            plot = fig.to_html(full_html=False)
            figure_dict.update({f"plot{index}": plot})
            index += 1

        context = {
            "user": request.user  # user, not username because we
                                  # need to check the user's attributes                                  
            } | figure_dict
        return render(request, template_name, context=context)
