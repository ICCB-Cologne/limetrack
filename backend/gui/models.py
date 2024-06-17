from django.db import models
from django.core.exceptions import ValidationError
import re
from .utils.model_choices import (LOCALISATION_CHOICE, SITE_CHOICES,
                                  SEX_CHOICES,
                                  TISSUE_TYPES, INTERVENTION_TYPES,
                                  CORRESPONDING_ORGANOID_CHOICES,
                                  GRADING,
                                  SPL_SEQUENCING_TYPES,
                                  SPL_STATUS_CHOICES,
                                  SCLAB_SEQUENCING_TYPES,
                                  SCLAB_STATUS_CHOICES,
                                  LB_ANALYTE_TYPES,
                                  LB_STATUS_CHOICES,
                                  SPATIAL_METHOD,
                                  SPATIAL_STATUS)

CHARFIELD_MAXLEN = 200


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


def check_sat3_sample_code(string):
    regex = \
     "^S3[MCP]-[a-zA-Z0-9]{5}-\\d+-[BTMXLNCFR]\\d+-[SVFPYO]-[DRCWYTMLGHN]\\d+$"
    if not re.search(regex, string):
        raise ValidationError("No valid Saturn3 Sample Code")


def check_sat3_sample_code_with_none_analyte(string):
    regex = "^S3[MCP]-[a-zA-Z0-9]{5}-\\d+-[BTMXLNCFR]\\d+-[SVFPYO]-[N]$"
    if not re.search(regex, string):
        raise ValidationError("No valid Saturn3 Sample Code")


def check_six_figures(number: str):
    return len(number) == 6

# Create your models here.


class HistopathologicalSample(models.Model):
    """
    When adding fields to the model,
    remember to make changes to
    the forms.py file accordingly.

    Meaning: go to forms.py and make sure
    that the lists and dicts on the top of
    the file include all model fields.
    """

    def generate_patient_id(self):
        return self.patient_identifier + self.recruiting_site

    # recruiter - 11 fields ###

    recruiting_site = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=SITE_CHOICES,
        verbose_name="Recruiting Site")

    patient_identifier = models.CharField(
        max_length=5,
        validators=[validate_alphanumeric],
        verbose_name="Patient Identifier")

    # patient = models.CharField( max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    sex = models.CharField(max_length=CHARFIELD_MAXLEN, choices=SEX_CHOICES,
                           verbose_name="Sex")
    died = models.DateField(null=True, blank=True, verbose_name="Died")
    # tissue_name = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    # used_in = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    saturn3_sample_code = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        validators=[check_sat3_sample_code],
        verbose_name="SATURN3 Sample Code",
        help_text="S3 + Entity - "
                  "Patient Identifier - "
                  "Sampling Timepoint - "
                  "Tissue Type + Order Number - "
                  "Storage Format - Analyte Type "
                  "+ Order Number")

    note = models.TextField(
        max_length=350,
        verbose_name="Note", blank=True,
        null=True)

    sampling_date = models.DateField(verbose_name="Sampling Date")
    tissue_type = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        choices=TISSUE_TYPES,
        verbose_name="Tissue Type")
    type_of_intervention = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=INTERVENTION_TYPES,
        verbose_name="Type of Intervention")
    localisation = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=LOCALISATION_CHOICE,
        verbose_name="Localisation")
    corresponding_organoid = models.BooleanField(
        verbose_name="Corresponding Organoid",
        choices=CORRESPONDING_ORGANOID_CHOICES
    )
    grading = models.CharField(max_length=CHARFIELD_MAXLEN, choices=GRADING,
                               verbose_name="Grading", blank=True,
                               null=True)
    # histology_subtype = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype

    # TUM Pathology ###
    tumor_cell_content = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True, null=True,
        validators=[zero_to_a_hundred],
        verbose_name="Tumor Cell Content")

    # SPL ###
    spl_received = models.DateField(
        null=True, blank=True, verbose_name="SPL Received")
    spl_status = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True, null=True,
        choices=SPL_STATUS_CHOICES,
        verbose_name="SPL Status")
    spl_sequencing_type = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True, null=True,
        choices=SPL_SEQUENCING_TYPES,
        verbose_name="SPL Sequencing Type")

    # scLab ###
    sclab_received = models.DateField(
        null=True, blank=True, verbose_name="scLab Received")
    sclab_extraction_date = models.DateField(null=True,
                                             blank=True,
                                             verbose_name="scLab "
                                                          "Extraction Date")
    sclab_nuclei_yield = models.IntegerField(null=True,
                                             blank=True,
                                             verbose_name="scLab Nuclei Yield")
    sclab_nuclei_size = models.IntegerField(null=True,
                                            blank=True,
                                            verbose_name="scLab particles "
                                                         "above 5 µm [%]")
    sclab_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                    blank=True, null=True,
                                    verbose_name="scLab Status",
                                    choices=SCLAB_STATUS_CHOICES)
    sclab_sequencing_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                             blank=True, null=True,
                                             verbose_name="scLab"
                                                          " Sequencing Type",
                                             choices=SCLAB_SEQUENCING_TYPES)
    sclab_sorting = models.BooleanField(choices=CORRESPONDING_ORGANOID_CHOICES,
                                        blank=True, null=True,
                                        verbose_name="scLab Sorting")
    sclab_pool = models.CharField(
        null=True,
        blank=True,
        verbose_name="scLab Pool")

    rna_isle_id = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        validators=[check_six_figures],
        verbose_name="RNA ILSE ID")

    atac_isle_id = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        validators=[check_six_figures],
        verbose_name="ATAC ILSE ID")

    sclab_comment = models.TextField(max_length=CHARFIELD_MAXLEN,
                                     blank=True,
                                     null=True,
                                     verbose_name="scLab Comment"
                                     )

    # Spatial ###
    spatial_method = models.CharField(blank=True, null=True,
                                      verbose_name="Spatial Method",
                                      choices=SPATIAL_METHOD)

    spatial_status = models.CharField(blank=True, null=True,
                                      verbose_name="Spatial Status",
                                      choices=SPATIAL_STATUS)

    xenium_run_date = models.DateField(null=True,
                                       blank=True,
                                       verbose_name="Xenium Run Date")

    xenium_slide_id = models.CharField(blank=True, null=True,
                                       verbose_name="Xenium Slide ID")

    xenium_run_id = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Xenium Run ID")

    xenium_panel_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Xenium Panel ID")

    merscope_run_date = models.DateField(blank=True, null=True,
                                         verbose_name="Merscope Run Date")

    merscope_run_id = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Merscope Run ID")

    merscope_panel_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Merscope Panel ID")

    dv_200 = models.CharField(blank=True, null=True,
                              verbose_name="DV200")

    spatial_comment = models.TextField(blank=True, null=True,
                                       verbose_name="Spatial Comment")

    # LB ###
    lb_analyte_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                       blank=True, null=True,
                                       verbose_name="LB analyte type",
                                       choices=LB_ANALYTE_TYPES)
    lb_sampling_date = models.DateField(null=True,
                                        blank=True,
                                        verbose_name="LB Sampling Date")
    lb_received = models.DateField(null=True,
                                   blank=True, verbose_name="LB Received")
    lb_sample_volume = models.IntegerField(null=True,
                                           blank=True,
                                           verbose_name="LB Sample"
                                                        " Volume [ml]")
    lb_date_of_isolation = models.DateField(null=True,
                                            blank=True,
                                            verbose_name="LB Date "
                                                         "of Isolation")
    lb_total_isolated_cfdna = \
        models.IntegerField(null=True, blank=True,
                            verbose_name="LB Total Isolated cfDNA [ng]")

    lb_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                 blank=True, null=True,
                                 verbose_name="LB Status",
                                 choices=LB_STATUS_CHOICES)

    # Datapaths ###

    pools = models.CharField(
        blank=True,
        null=True,
        verbose_name="Pools")
    scrna_r1 = models.CharField(
        blank=True,
        null=True,
        verbose_name="scRNA R1")

    scrna_r2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="scRNA R2")
    scatac_r1 = models.CharField(
        blank=True,
        null=True,
        verbose_name="scATAC R1")

    scatac_r2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="scATAC R2")

    scatac_i2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="scATAC I2")

    wgs_r1 = models.CharField(
        blank=True,
        null=True,
        verbose_name="WGS R1")

    wgs_r2 = models.CharField(blank=True,
                              null=True,
                              verbose_name="WGS R2")

    wgs_bam = models.CharField(blank=True,
                               null=True,
                               verbose_name="WGS bam")

    wgs_vcf = models.CharField(blank=True,
                               null=True,
                               verbose_name="WGS vcf")
