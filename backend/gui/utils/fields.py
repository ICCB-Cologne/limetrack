from collections.abc import Sequence
from typing import Any
from django.forms.fields import (MultiValueField, CharField,
                                 IntegerField, ChoiceField)
from django.forms import Select, MultiWidget, TextInput, NumberInput
from backend.gui.models import validate_alphanumeric
import re

ENTITY = [
    ("S3M", "M"),
    ("S3C", "C"),
    ("S3P", "P")
]

TISSUE_TYPE = [
    ("B", "B"),
    ("T", "T"),
    ("M", "M"),
    ("S", "S"),
    ("X", "X"),
    ("L", "L"),
    ("N", "N"),
    ("C", "C"),
    ("F", "F"),
    ("R", "R"),
]

STORAGE_FORMAT = [
    ("S", "S"),
    ("V", "V"),
    ("F", "F"),
    ("P", "P"),
    ("Y", "Y")
    ]

ANALYTE_TYPE = [
    ("D", "D"),
    ("R", "R"),
    ("C", "C"),
    ("W", "W"),
    ("Y", "Y"),
    ("T", "T"),
    ("M", "M"),
    ("L", "L"),
    ("G", "G"),
    ("H", "H"),
    ("N", "N"),
]


class CustomSelect(Select):
    def __init__(self,
                 attrs: dict[str, Any] | None = ...,
                 choices: Sequence[tuple[Any, Any]] = ...) -> None:
        super().__init__(attrs, choices)


class SampleCodeField(MultiValueField):
    """
    Supposed to split the Saturn3-Sample-Code field into 8 different fields
    """
    def __init__(self, **kwargs):

        error_messages = {
            "incomplete": "Choose or enter a value for every field.",
        }

        fields = (
            ChoiceField(
                error_messages={"incomplete": "Select a value"},
                choices=ENTITY
            ),

            CharField(
                max_length=5,
                error_messages={"incomplete": "Enter a 5-digit PID"},
                validators=[validate_alphanumeric],
                help_text="Saturn3 + Entity"
            ),

            IntegerField(
                error_messages={"incomplete": "Enter integer"},
                min_value=0),

            ChoiceField(
                error_messages={"incomplete": "Select a value"},
                choices=TISSUE_TYPE
            ),

            IntegerField(
                error_messages={"incomplete": "Enter integer"},
                min_value=0),

            ChoiceField(
                error_messages={"incomplete": "Select a value"},
                choices=STORAGE_FORMAT
            ),

            ChoiceField(
                error_messages={"incomplete": "Select a value"},
                choices=ANALYTE_TYPE
            ),

            IntegerField(error_messages={"incomplete": "Enter integer"},
                         min_value=0),
        )

        super().__init__(
            error_messages=error_messages,
            fields=fields,
            require_all_fields=True,
            **kwargs,
            )

    def compress(self, valid_values: list):
        string = ""
        for v in valid_values:
            string += str(v)
            if valid_values.index(v) != 3 and valid_values.index(v) != 6:
                string += "-"
        return string[:-1]


class SampleCodeWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None) -> None:

        widgets = [
            Select(
                attrs=attrs,
                choices=ENTITY),

            TextInput(
                attrs={"maxlength": 5,
                       "data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "5-digit SATURN3 pseudonym (by Treuhandstelle Freiburg)"}
                             ),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Sampling timepoint 0, 1, 2 etc."}),

            Select(
                attrs=attrs,
                choices=TISSUE_TYPE),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Tissue type - order number"}),

            Select(choices=STORAGE_FORMAT),

            Select(choices=ANALYTE_TYPE),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Analyte type - order number"})]

        super().__init__(widgets, attrs)

    def decompress(self, value: Any) -> Any | None:
        if isinstance(value, str) and value != "None-None-None-None-None-None-None-None":
            splitted = re.split('-', value)
            res = []
            section: str
            for section in splitted:
                if section.isnumeric():
                    res.append(int(section))
                elif (splitted.index(section) == 3 or
                      splitted.index(section) == 5):
                    res.append(section[0])
                    res.append(int(section[1:]))
                else:
                    res.append(section)
            return res
        return [None] * 8

    def value_from_datadict(self,
                            data: dict[str, Any],
                            files,
                            name: str) -> Any:
        """
        Handles the data dict coming from a submitted form or from the database
        """
        if "saturn3_sample_code" in data:
            return self.decompress(data["saturn3_sample_code"])
        decompressed_list = []
        decompressed_list.append(data["saturn3_sample_code_0"])
        decompressed_list.append(data["saturn3_sample_code_1"])
        decompressed_list.append(data["saturn3_sample_code_2"])
        decompressed_list.append(data["saturn3_sample_code_3"])
        decompressed_list.append(data["saturn3_sample_code_4"])
        decompressed_list.append(data["saturn3_sample_code_5"])
        decompressed_list.append(data["saturn3_sample_code_6"])
        decompressed_list.append(data["saturn3_sample_code_7"])
        return decompressed_list
