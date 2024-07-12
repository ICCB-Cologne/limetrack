from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse
)
from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.files import File

from typing import Any
import logging

app_log = logging.getLogger("s3sample")


class FAQView(LoginRequiredMixin, TemplateView):
    def get(
            self,
            request: HttpRequest,
            *args: Any,
            **kwargs: Any
    ) -> HttpResponse:
        template_name = "gui/faq.html"
        context = {
            "user": request.user.get_username()
        }

        return render(request, template_name, context=context)


class ContactView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:

        template_name = "gui/contact.html"
        return render(request, template_name)


class HomeView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        template_name = "gui/home.html"
        context = {}

        with open("CHANGELOG.md", "r") as fh:
            myfile = File(fh)
            context["changelog"] = myfile.read()

        return render(request, template_name, context=context)


class ImprintView(TemplateView):
    def get(self, request: HttpRequest,
            *args: Any, **kwargs: Any) -> HttpResponse:

        template_name = "gui/imprint.html"
        context = {
            "user": request.user.get_username()
        }

        return render(request, template_name, context=context)
