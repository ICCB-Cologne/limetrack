from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files import File
from django.http import (
    HttpRequest,
    HttpResponse
)
from typing import Any


class HomeView(LoginRequiredMixin, TemplateView):
    def get(self,
            request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/home.html"
        context = {}

        with open("CHANGELOG.md", "r") as fh:
            myfile = File(fh)
            context["changelog"] = myfile.read()

        return render(request, template_name, context=context)
