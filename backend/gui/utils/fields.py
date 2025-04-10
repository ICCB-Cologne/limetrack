"""
This module contains the handling of the SATURN3 Sample Code field.

The process of converting a field composed of
multiple dropdown and number fields
into a coherent string value in the database,
and the other way round, is a bit complicated.
The value_from_datadict & decompress functions take care of that.
"""

from collections.abc import Sequence
from typing import Any
from django.forms.fields import (MultiValueField, CharField,
                                 IntegerField, ChoiceField)
from django.forms import Select, MultiWidget, TextInput, NumberInput
from utils.validators import validate_alphanumeric
from django.utils.datastructures import MultiValueDictKeyError
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
    ("Y", "Y"),
    ("O", "O")
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
    Splits the Saturn3-Sample-Code field into 8 different fields
    """
    def __init__(self, **kwargs):

        error_messages = {
            "incomplete": "Choose or enter a value for every field.",
        }

        fields = (
            ChoiceField(
                error_messages={"incomplete": "Select an entity value"},
                choices=ENTITY
            ),

            CharField(
                max_length=5,
                error_messages={"incomplete": "Enter a 5-digit PID"},
                validators=[validate_alphanumeric],
                help_text="Saturn3 + Entity"
            ),

            IntegerField(
                error_messages={"incomplete": "Enter sampling timepoint"},
                min_value=0),

            ChoiceField(
                error_messages={"incomplete": "Select a tissue type value"},
                choices=TISSUE_TYPE
            ),

            IntegerField(
                error_messages={
                    "incomplete": "Enter tissue type order number"},
                min_value=0),

            ChoiceField(
                error_messages={"incomplete": "Select a storage format value"},
                choices=STORAGE_FORMAT
            ),

            ChoiceField(
                error_messages={"incomplete": "Select an analyte type value"},
                choices=ANALYTE_TYPE
            ),

            IntegerField(
                error_messages={
                    "incomplete": "Enter analyte type order number"},
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
        index = 0
        for v in valid_values:
            string += str(v)
            if index != 3 and index != 6:
                string += "-"
            index += 1
        return string[:-1]


class SampleCodeWidget(MultiWidget):
    """
    Widget representing the SATURN3-Sample-Code field.
    """

    def __init__(self, disabled=False, widgets=None, attrs=None) -> None:

        disabled = {"disabled": "true"} if disabled else {}

        widgets = [
            Select(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Entity"} | disabled,
                choices=ENTITY),

            TextInput(
                attrs={
                    "maxlength": 5,
                    "data-toggle": "tooltip",
                    "data-placement": "top",
                    "title": "5-digit SATURN3 \
                        pseudonym (by Treuhandstelle Freiburg)"}
                | disabled
                ),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Sampling timepoint 0, 1, 2 etc.",
                       "min": "0"} | disabled),

            Select(
                attrs={
                    "data-toggle": "tooltip",
                    "data-placement": "top",
                    "title": "Tissue type"}
                | disabled,
                choices=TISSUE_TYPE),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Tissue type - order number",
                       "min": "0"} | disabled),

            Select(
                attrs={
                    "data-toggle": "tooltip",
                    "data-placement": "top",
                    "title": "Storage format"}
                | disabled,
                choices=STORAGE_FORMAT),

            Select(
                attrs={
                    "data-toggle": "tooltip",
                    "data-placement": "top",
                    "title": "Analyte type"}
                | disabled,
                choices=ANALYTE_TYPE),

            NumberInput(
                attrs={"data-toggle": "tooltip",
                       "data-placement": "top",
                       "title": "Analyte type - order number",
                       "min": "0"} | disabled)]

        super().__init__(widgets, attrs)

    def decompress(self, value: Any) -> Any | None:
        if (isinstance(value, str) and
                value != "None-None-None-None-None-None-None-None"):
            splitted = re.split('-', value)
            res = []
            section: str
            for section in splitted:
                if section.isnumeric():
                    res.append(int(section))
                elif (splitted.index(section) == 3 or
                      splitted.index(section) == 5):
                    res.append(section[0])
                    if len(section) > 1:
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
        try:
            decompressed_list.append(data["saturn3_sample_code_0"])
            decompressed_list.append(data["saturn3_sample_code_1"])
            decompressed_list.append(data["saturn3_sample_code_2"])
            decompressed_list.append(data["saturn3_sample_code_3"])
            decompressed_list.append(data["saturn3_sample_code_4"])
            decompressed_list.append(data["saturn3_sample_code_5"])
            decompressed_list.append(data["saturn3_sample_code_6"])
            decompressed_list.append(data["saturn3_sample_code_7"])
        except MultiValueDictKeyError:
            return decompressed_list
        return decompressed_list
