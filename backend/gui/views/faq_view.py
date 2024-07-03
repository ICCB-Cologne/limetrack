from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpRequest, HttpResponse
)
from django.views.generic import TemplateView
from django.shortcuts import render

from typing import Any


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
