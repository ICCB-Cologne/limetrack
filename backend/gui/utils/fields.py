from collections.abc import Sequence
from typing import Any
from django.forms.fields import MultiValueField, CharField, IntegerField, ChoiceField
from django.forms import Select, MultiWidget, TextInput, NumberInput
from django.forms.widgets import Widget
from backend.gui.models import validate_alphanumeric
import re

ENTITY = [
    ("S3M", "S3M"),
    ("S3C", "S3C"),
    ("S3P", "S3P")
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




class SampleCodeField(MultiValueField):
    def __init__(self, **kwargs):

        fields = (
            ChoiceField(
                error_messages={"incomplete": "Select a value"},choices=ENTITY
            ),
            CharField(
                error_messages={"incomplete": "Enter a 5-digit PID"},
                validators=[validate_alphanumeric], help_text="Saturn3 + Entity"
            ),
            CharField(error_messages={"incomplete": "Enter integer"}),

            ChoiceField(
                error_messages={"incomplete": "Select a value"},choices=TISSUE_TYPE
            ),

            CharField(error_messages={"incomplete": "Enter integer"}),

            ChoiceField(
                error_messages={"incomplete": "Select a value"}, choices=STORAGE_FORMAT
            ),

            ChoiceField(
                error_messages={"incomplete": "Select a value"}, choices=ANALYTE_TYPE
            ),

            CharField(error_messages={"incomplete": "Enter integer"}),
            
        )
        
        super().__init__(
            fields=fields,
            require_all_fields=True,
            **kwargs,
            widget=SampleCodeWidget())
        

    def compress(self, valid_values: list):
        string = ""
        for v in valid_values:
            string += str(v)
            if valid_values.index(v) != 3 and valid_values.index(v) != 6:
                string += "-"
        return string[:-1]

class SampleCodeWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None) -> None:
        widgets=[
            Select(attrs=attrs, choices=ENTITY),
            TextInput(attrs=attrs,),
            TextInput(attrs=attrs,),
            Select(attrs=attrs, choices=TISSUE_TYPE), 
            TextInput(attrs=attrs),
            Select(choices=STORAGE_FORMAT),
            Select(choices=ANALYTE_TYPE),
            TextInput(attrs=attrs)]
        
        super().__init__(widgets, attrs)

    def decompress(self, value: Any) -> Any | None:
        if isinstance(value, str):
            splitted = re.split('-', value)
            print(splitted)
            res = []
            i: str
            for i in splitted:
                if i.isalnum():
                    res.append(i)
            return res
        
        return [None] * 8