from django.core.exceptions import ValidationError
import re


def validate_alphanumeric(value):
    char: str
    if len(value) < 5:
        raise ValidationError("Lenght has to be exactly 5 characters")
    for char in value:
        if not char.isalnum():
            raise ValidationError("Only letters and numbers allowed")


def zero_to_a_hundred(value):
    if type(value) is not int:
        try:
            int(value)
        except ValueError:
            raise ValidationError("Only integer numbers are allowed")
    if int(value) < 0 or int(value) > 100:
        raise ValidationError("Value between 0 and 100")


def one_to_five(value):
    if type(value) is not int:
        try:
            int(value)
        except ValueError:
            raise ValidationError("Only integer numbers are allowed")
    if int(value) < 1 or int(value) > 5:
        raise ValidationError("Value between 1 and 5")


def check_sat3_sample_code(string):
    regex = \
     "^S3[MCP]-[a-zA-Z0-9]{5}-\\d+-[BTMXLNCFR]\\d+-[SVFPYO]-[DRCWYTMLGHN]\\d+$"
    if not re.search(regex, string):
        raise ValidationError("No valid Saturn3 Sample Code")


def check_sat3_sample_code_with_none_analyte(string):
    regex = "^S3[MCP]-[a-zA-Z0-9]{5}-\\d+-[BTMXLNCFR]\\d+-[SVFPYO]-[N]$"
    if not re.search(regex, string):
        raise ValidationError("No valid Saturn3 Sample Code")


def check_eleven_figures(number: str):
    if len(number) != 11 and len(number) != 5:
        error_mesage = "Value has to consist of exactly 5 or 11 characters"
        raise ValidationError(error_mesage)


def no_commas_allowed(comment: str):
    if "," in comment:
        raise ValidationError("Commas are not permitted.")
