from django.contrib.auth.mixins import LoginRequiredMixin
from pydantic import BaseModel, ValidationError, EmailStr
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView
from django.db.utils import IntegrityError
from dataclasses import dataclass
from typing import Optional
from io import StringIO
from enum import Enum
import pandas as pd
import logging
import json


class UserGroup(str, Enum):
    READONLY = "ReadOnly"
    ADMINS = "admins"
    COORDINATORS = "coordinators"
    LIQUIDBIOPSY = "LiquidBiopsy"
    SCOPENLAB = "scOpenLab"
    SPL = "SPL"
    TUM = "TUM"
    RECRUITER = "Recruiter"
    OMICSPATH = "OmicsPath"
    SPATIAL = "Spatial"


class UserSchema(BaseModel):
    username: EmailStr
    first_name: str
    last_name: str
    group: UserGroup


@dataclass
class Error:
    name: str
    description: str
    severity: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "severity": self.severity
        }


logger = logging.getLogger("s3sample")


class UsersBulkView(LoginRequiredMixin, TemplateView):
    def _append_and_log_error(
        self,
        name: str,
        description: str,
        errors: list[Error],
        level: int = logging.INFO,
    ) -> list[Error]:
        errors.append(
            Error(
                name=name,
                description=description,
                severity=logging.getLevelName(level)
            )
        )
        logger.log(level=level, msg=f"{name}: {description}")

        return errors

    def _build_response_json(self,
                             created: list[str], errors: list[Error]) -> str:
        response = {
            "created": created,
            "errors": list(
                map(
                    lambda e: e.to_dict(),
                    errors
                )
            )
        }

        return json.dumps(response)

    def post(self, request: HttpRequest) -> HttpResponse:
        data: Optional[str] = request.POST.get("data")
        errors: list[Error] = []
        created: list[str] = []

        if data:
            with StringIO(data) as buffer:
                df = pd.read_csv(buffer)
                for _, row in df.iterrows():
                    try:
                        user_schema = UserSchema(**row.to_dict())

                        user = User.objects.create_user(
                            username=user_schema.username,
                            first_name=user_schema.first_name,
                            last_name=user_schema.last_name,
                            email=user_schema.username
                        )

                        g = Group.objects.get(name=user_schema.group.value)
                        user.groups.add(g)

                        user.save()
                        created.append(user.username)

                    except (ValidationError, IntegrityError) as e:
                        name = type(e).__name__
                        description = str(e)
                        errors = self._append_and_log_error(name,
                                                            description,
                                                            errors)

        else:
            name = "Missing Data"
            description = "Upload does not contain any data"
            errors = self._append_and_log_error(name, description, errors)

        return HttpResponse(content=self._build_response_json(created, errors))
