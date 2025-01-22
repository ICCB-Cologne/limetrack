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
                                  SPATIAL_STATUS,
                                  SCANALYSIS_CHOICES,
                                  LB_SEQUENCING_STATUS_CHOICES)

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
        raise ValidationError("Value has to consist of exactly 5 or 11 characters")
    
def no_commas_allowed(comment: str):
    if "," in comment:
        raise ValidationError("Commas are not permitted.")

# Create your models here.


class HistopathologicalSample(models.Model):
    """
    When adding fields to the model,
    remember to make changes to
    the forms.py file accordingly.

    Meaning: go to forms.py and make sure
    that the lists and dicts on the top of
    the file include all model fields.
    If you add date fields give them a DatePicker widget.
    
    Don't forget to change the downloadable template csv file (views/download_views.py)
    and to adapt the test csv files (at least the one_record.csv file).


    Last but not least include the new fields into the selenium tests. (gui/selenium/)

    """

    class Meta:

        # naming constraints:
        # official group name found in admin console + _fields e.g. recruiter_fields
        permissions = [
            ("recruiter_fields", "Can edit empty recruiter fields & create records."),
            ("tum_fields", "Can edit empty TUM fields."),
            ("spl_fields", "Can edit empty SPL fields."),
            ("scopenlab_fields", "Can edit empty SCLab fields."),
            ("spatial_fields", "Can edit empty Spatial fields."),
            ("liquidbiopsy_fields", "Can edit empty LB fields."),
            ("omicspath_fields", "Can edit empty Omics fields."),
            # ("readonly", "Can only read data."),
            # ("all_fields", "Can edit all empty fields.")
        ]

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
        null=True,
        validators=[no_commas_allowed])

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

    tissue_quality = models.IntegerField(
        blank=True, null=True,
        validators=[one_to_five],
        verbose_name="Tissue Quality"
        )

    tumor_cell_content = models.CharField(
        blank=True, null=True,
        validators=[zero_to_a_hundred],
        verbose_name="Tumor Cell Content")

    percent_avital_cells = models.IntegerField(
        blank=True, null=True,
        validators=[zero_to_a_hundred],
        verbose_name="Percentage avital cells")

    comment_tumor_cell_content = models.TextField(
        blank=True, null=True,
        verbose_name="Comment tumor cell content",
        validators=[no_commas_allowed])

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
        verbose_name="SPL Analysis Type")

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
        max_length=11,
        validators=[check_eleven_figures],
        verbose_name="RNA ILSE ID")

    atac_isle_id = models.CharField(
        null=True,
        blank=True,
        max_length=11,
        validators=[check_eleven_figures],
        verbose_name="ATAC ILSE ID")

    sclab_comment = models.TextField(max_length=CHARFIELD_MAXLEN,
                                     blank=True,
                                     null=True,
                                     verbose_name="scLab Comment",
                                     validators=[no_commas_allowed]
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
                                       max_length=10,
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
                              max_length=3,
                              verbose_name="DV200",
                              validators=[zero_to_a_hundred])

    spatial_comment = models.TextField(blank=True, null=True,
                                       verbose_name="Spatial Comment",
                                       validators=[no_commas_allowed])

    # LB ###
    lb_analyte_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                       blank=True, null=True,
                                       verbose_name="LB analyte type",
                                       choices=LB_ANALYTE_TYPES)
    lb_panel_r1 = models.CharField(blank=True, null=True,
                                   verbose_name="LB panel R1")
    
    lb_panel_r2 = models.CharField(blank=True, null=True,
                                   verbose_name="LB panel R2")

    lb_sequencing_status = models.CharField(blank=True, null=True,
                                            verbose_name="LB Sequencing Status",
                                            choices=LB_SEQUENCING_STATUS_CHOICES)

    lb_received = models.DateField(null=True,
                                   blank=True, verbose_name="LB Received")
    lb_sample_volume = models.DecimalField(null=True, max_digits=4, decimal_places=1,
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

    request_execution_of = models.CharField(
        blank=True,
        null=True,
        verbose_name="Request execution of"
    )

    cell_ranger_arc_run = models.DateField(
        blank=True,
        null=True,
        verbose_name="Cellranger-arc run"
    )

    sc_analysis_status = models.CharField(
        blank=True,
        null=True,
        verbose_name="scAnalysis status",
        choices=SCANALYSIS_CHOICES)

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

    # Timestamp ###

    created = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name="Created at")