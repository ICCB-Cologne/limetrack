from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse)
from django.views.generic import TemplateView
from django.shortcuts import render
from ..models import HistopathologicalSample
from typing import Any
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

coordinates = {
    "Göttingen": (51.542674085238346, 9.913804090413405),
    "Heidelberg": (49.39899667646808, 8.672968635087408),
    "Essen": (51.45191841759816, 7.011888831333727),
    "Köln": (50.936388829448646, 6.958386355628797),
    "Frankfurt": (50.1153717270215, 8.687365774626162),
    "München": (48.13357641953071, 11.579255350658212),
    "Augsburg": (48.36831813866189, 10.900568819747098),
}

token = "pk.eyJ1IjoiamctaWJzbSIsImEiOiJjbHlxeDU0YWkwMHNnMnJzNzd0aGZtMng4In0.qnb1sMw30ZLEm4Le6EwISw"


def count_samples_by_category(samples: list[HistopathologicalSample]):

    headings = {"recruiting_site": "Samples by recruiting site",
                "saturn3_sample_code": "Samples by entity - total"}

    plot_dicts = []

    count_by = ["saturn3_sample_code", "recruiting_site"]

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

        fig = go.Figure(
            data=[go.Bar(x=list(counter_dict.keys()),
                         y=list(counter_dict.values()),
                         marker_color="#142a62", opacity=0.8)])

        fig.update_xaxes(type='category')
        fig.update_xaxes(categoryorder='total descending')

        plot = fig.to_html(full_html=False)
        plot_dicts.append({"plot": plot, "heading": headings[c]})

    return plot_dicts


def count_samples_by_site_and_entity(samples: list[HistopathologicalSample]):

    data = {"Site": [], "Entity": [], "Count": []}

    site_sample_pairs = [
        [getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name == "recruiting_site" or
            field.name == "saturn3_sample_code"]
        for instance in samples
    ]

    entity_counter = {}
    for sample in site_sample_pairs:
        site = sample[0]
        if site not in entity_counter:
            entity_counter.update({sample[0]: [0, 0, 0]})
        entity = sample[1][0:3]
        if entity == "S3C":
            entity_counter[site][0] += 1
        elif entity == "S3M":
            entity_counter[site][1] += 1
        elif entity == "S3P":
            entity_counter[site][2] += 1

    for site in entity_counter.keys():
        data["Site"].append(site)
        data["Entity"].append("S3C")
        data["Count"].append(entity_counter[site][0])
        data["Site"].append(site)
        data["Entity"].append("S3M")
        data["Count"].append(entity_counter[site][1])
        data["Site"].append(site)
        data["Entity"].append("S3P")
        data["Count"].append(entity_counter[site][2])

    fig = px.bar(data, x="Site", y="Count", color="Entity",
                 color_discrete_sequence=["#142a62", "#64cad3", "#e2e2cf"],
                 opacity=0.8)
    fig.update_xaxes(type='category')
    fig.update_xaxes(categoryorder='total descending')
    return fig.to_html()


def sample_process_plot(samples: list[HistopathologicalSample]):
    data = {"received at": ["none", "spl", "sclab"],
            "number": [0, 0, 0]}

    received_dates = [
        [getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name == "spl_received" or
            field.name == "sclab_received"]
        for instance in samples
    ]

    for dates in received_dates:
        if dates[1]:
            data["number"][2] += 1
        elif dates[0]:
            data["number"][1] += 1
        else:
            data["number"][0] += 1

    fig = px.pie(data, values='number', names='received at', opacity=0.8,
                 color_discrete_sequence=["#142a62", "#64cad3", "#e2e2cf"])
    return fig.to_html


def map_plot(samples: list[HistopathologicalSample]):

    data = {"lat": [], "lon": [], "Samples": [], "site": []}

    key_value_pairs = [
            [getattr(instance, field.name)
                for field in instance._meta.fields
                if field.name == "recruiting_site"]
            for instance in samples
        ]
    keys = [site[0] for site in key_value_pairs]
    keys = list(set(keys))
    counter_dict = dict()

    for key in keys:
        counter_dict.update({key: 0})

    for key_value in key_value_pairs:
        counter_dict[key_value[0]] += 1

    for site in counter_dict:
        data["site"].append(site)
        data["Samples"].append(counter_dict[site])
        data["lat"].append(coordinates[site][0])
        data["lon"].append(coordinates[site][1])

    df = pd.DataFrame(data=data)

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="Samples",
                            hover_name="site",
                            hover_data={"Samples": True,
                                        "lat": False,
                                        "lon": False},
                            color_discrete_sequence=["#142a62"], zoom=5.5,
                            center=dict(lat=51.19, lon=10.459),
                            height=800, width=700)

    fig.update_layout(mapbox_style="outdoors", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20})
    fig.update_layout(mapbox_bounds={"west": 3, "east": 18,
                                     "south": 47.1, "north": 55.2})
    return fig.to_html(full_html=False)


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

        figure_list = []
        for dic in plot_dict:

            figure_list.append(dic)

        map_plot1 = map_plot(samples)
        figure_list.append({"heading": "Samples by sites - Map",
                            "plot": map_plot1})

        figure_list.append({"heading": "Sample by entity and site",
                            "plot": count_samples_by_site_and_entity(samples)})

        figure_list.append({"heading": "Sample Processing",
                            "plot": sample_process_plot(samples)})

        context = {
            "user": request.user,  # user, not username because we
                                   # need to check the user's attributes
            "figure_list": figure_list
            }
        return render(request, template_name, context=context)
