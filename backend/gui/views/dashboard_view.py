from django.contrib.auth.mixins import LoginRequiredMixin
from backend.gui.utils.colors import Saturn3Colors
from django.http import HttpRequest, HttpResponse
from django.views.generic import TemplateView
from ..models import HistopathologicalSample
from django.db.models import QuerySet
from django.shortcuts import render
import plotly.graph_objects as go                               # type: ignore
from django.conf import settings
import plotly.express as px                                     # type: ignore
from typing import Any
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

entity_dict = {"S3M": "BC", "S3P": "PDAC", "S3C": "CRC"}

token = settings.SETTINGS.MAPPLOT_TOKEN


def count_samples_by_category(samples: QuerySet[HistopathologicalSample, HistopathologicalSample]):
    headings = {
        "recruiting_site": "Samples by recruiting site",
        "saturn3_sample_code": "Samples by entity - total",
    }
    plot_dicts: list[dict[str, str | dict[str, str]]] = []
    count_by = ["saturn3_sample_code"]

    for c in count_by:
        key_value_pairs = [
            [
                getattr(instance, field.name)
                for field in instance._meta.fields
                if field.name == c
            ]
            for instance in samples
        ]
        keys = [site[0] for site in key_value_pairs]
        keys = list(set(keys))
        counter_dict = dict()

        for key in keys:
            if c == "saturn3_sample_code":
                # count entities (S3C, S3P, S3M)
                key = entity_dict[key[:3]]
            counter_dict.update({key: 0})

        for key_value in key_value_pairs:
            if c == "saturn3_sample_code":
                counter_dict[entity_dict[key_value[0][:3]]] += 1
            else:
                counter_dict[key_value[0]] += 1

        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(counter_dict.keys()),
                    y=list(counter_dict.values()),
                    marker_color=Saturn3Colors.DARK_BLUE_HEX,
                    opacity=0.8,
                )
            ]
        )

        fig.update_xaxes(type="category")
        fig.update_xaxes(categoryorder="total descending")
        fig.update_xaxes(title_text="Entity")
        fig.update_yaxes(title_text="Number of samples")

        plot: str = fig.to_html(full_html=False)
        plot_dicts.append({"plot": plot, "heading": headings[c]})

    return plot_dicts


def count_samples_by_site_and_entity(samples: QuerySet[HistopathologicalSample, HistopathologicalSample]):
    data: dict[str, list] = {"Site": [], "Entity": [], "Number of samples": []}
    site_sample_pairs = [
        [
            getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name == "recruiting_site" or field.name == "saturn3_sample_code"
        ]
        for instance in samples
    ]
    entity_counter: dict[str, list[int]] = {}

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
        data["Entity"].append("CRC")
        data["Number of samples"].append(entity_counter[site][0])
        data["Site"].append(site)
        data["Entity"].append("BC")
        data["Number of samples"].append(entity_counter[site][1])
        data["Site"].append(site)
        data["Entity"].append("PDAC")
        data["Number of samples"].append(entity_counter[site][2])

    fig = px.bar(
        data,
        x="Site",
        y="Number of samples",
        color="Entity",
        color_discrete_sequence=[
            Saturn3Colors.DARK_BLUE_HEX,
            Saturn3Colors.AQUA_HEX,
            Saturn3Colors.KHAKI_HEX,
        ],
        opacity=0.8,
    )
    fig.update_xaxes(type="category")
    fig.update_xaxes(categoryorder="total descending")

    return fig.to_html()


def sample_process_plot(samples: QuerySet[HistopathologicalSample, HistopathologicalSample]):
    data: dict[str, list] = {"received at": ["none", "spl", "sclab", "wgs"],
            "number": [0, 0, 0, 0]}

    received_dates = [
        [
            getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name == "spl_received" or
            field.name == "sclab_received" or
            field.name == "wgs_bam"]
        for instance in samples
    ]

    for dates in received_dates:
        if dates[2] and dates[2] != "None":
            data["number"][3] += 1
        elif dates[1] and dates[1] != "None":
            data["number"][2] += 1
        elif dates[0] and dates[0] != "None":
            data["number"][1] += 1
        else:
            data["number"][0] += 1

    fig = px.pie(data, values='number', names='received at', opacity=0.8,
                 color_discrete_sequence=[Saturn3Colors.DARK_BLUE_HEX,
                                          Saturn3Colors.AQUA_HEX,
                                          Saturn3Colors.KHAKI_HEX,
                                          Saturn3Colors.BLUE_GREEN_HEX
                                          ],
                 height=800)
    fig.update_layout(margin_b=150, margin_t=150, margin_l=150, margin_r=150)

    return fig.to_html


def map_plot(samples: QuerySet[HistopathologicalSample, HistopathologicalSample]):
    data: dict[str, list] = {"lat": [], "lon": [], "Samples": [], "site": []}

    key_value_pairs = [
        [
            getattr(instance, field.name)
            for field in instance._meta.fields
            if field.name == "recruiting_site"
        ]
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

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="Samples",
        hover_name="site",
        hover_data={"Samples": True, "lat": False, "lon": False},
        color_discrete_sequence=[Saturn3Colors.DARK_BLUE_HEX],
        zoom=5,
        center=dict(lat=51.19, lon=10.459),
        height=800,
    )

    if token:
        fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)
    else:
        fig.update_layout(mapbox_style="carto-positron")

    fig.update_layout(margin={"r": 20, "t": 20, "l": 20, "b": 20})
    fig.update_layout(
        mapbox_bounds={"west": 3, "east": 18, "south": 47.1, "north": 55.2}
    )

    return fig.to_html(full_html=False)


class DashboardView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/dashboard.html"
        samples = HistopathologicalSample.objects.all()
        plot_dict = count_samples_by_category(samples)

        row1, row2 = [], []
        for dic in plot_dict:

            row1.append(dic)

        map_plot1 = map_plot(samples)
        row2.append({"heading": "Samples by sites - Map", "plot": map_plot1})

        row1.append(
            {
                "heading": "Samples by entity and site",
                "plot": count_samples_by_site_and_entity(samples),
            }
        )

        row2.append(
            {"heading": "Sample Processing", "plot": sample_process_plot(samples)}
        )

        context = {
            "user": request.user,  # user, not username because we
            # need to check the user's attributes
            "row1": row1,
            "row2": row2,
        }
        return render(request, template_name, context=context)
