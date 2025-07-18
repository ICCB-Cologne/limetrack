from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import validators
from django.utils.text import Truncator
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
                                  LB_SEQUENCING_STATUS_CHOICES,
                                  YES_NO_CHOICES)

CHARFIELD_MAXLEN = 200


# dictionary for splitting the model into sections
# keys: sections, values: put in the last field name of each section
# TODO: if no sections needed: handling of empty dict
# needs to be implemented in forms, views etc.
end_of_model_section_dict = {
    "recruiter": "grading",
    "tum": "comment_tumor_cell_content",
    "spl": "spl_sequencing_type",
    "scopenlab": "sclab_comment",
    "spatial": "spatial_comment",
    "liquidbiopsy": "lb_status",
    "omicspath": "wgs_ref",
}


class HistopathologicalSample(models.Model):
    """
    --- PERMISSION MANAGEMENT ---
    In the SATURN3 Sample Tracker the model is split into
    7 'sections' (e.g., SPL, Recruiter ...) which
    users can access only if they have the respective permissions.
    For the forms in the front-end this means, that form fields
    a user has no permissions to edit are greyed out and disabled.
    In the back-end, data input is handled in a similar way.
    Data is processed only for the sections a user has permissions to edit.

    2 fields are idependent of these sections and not editable:
    id (generated automatically by django)
    created (time stamp)

    New samples can only be created by users with the permission
    to create new records ("gui.add_histopathologicalsample" permission).
    Other users utilize the sat3 sample code
    to refer to existing samples in order to edit
    the sample's sections they're allowed to change.

    Data fields that are already filled with data can only
    be changed by users that have the
    "gui.change_histopathologicalsample" permission.

    --- IMPORTANT INSTRUCTIONS ---
    When adding fields to the model or
    especially creating a whole new model or multiple models,
    remember to make changes to the dependent code accordingly.

    Meaning: go to forms.py & utils/model_to_form and make sure
    the model is transformed to a form (or multiple forms) correctly.

    Don't forget to change the downloadable
    template csv file (views/download_views.py)
    and to adapt the test csv files (at least the one_record.csv file).

    Last but not least include the
    new fields into the selenium integration tests. (gui/selenium/)
    This includes also the create_test_users.py script for the github actions

    If your changes of the model affect the last field of a section:
    Edit the end_of_model_section_dict accordingly.

    --- APPLY YOUR OWN MODEL ---
    If you intend to use your own model and create a new class
    with a new name, note that LiMeTrack's code is build on this
    single django data model.
    Choosing a name different from HistopathologicalSample will result in
    having to make changes everywhere the model explicitly occurs
    in the project.
    """

    class Meta:
        """
        These permissions regulate which 'sections' of the model
        a user or a user group has access to
        naming constraints:
        official group/section name + _fields e.g. recruiter_fields
        """

        permissions = [
            ("recruiter_fields", "Recruiter fields permission"),
            ("tum_fields", "TUM fields permission"),
            ("spl_fields", "SPL fields permission"),
            ("scopenlab_fields", "ScLab fields permission"),
            ("spatial_fields", "Spatial fields permission"),
            ("liquidbiopsy_fields", "LB fields permission"),
            ("omicspath_fields", "OMICS fields permission"),
        ]

    # def save(self, *args, **kwargs):
    #     exact_lb_total_isolated_cfdna = Truncator(
    #         self.lb_total_isolated_cfdna).truncate_decimal(2)
    #     self.lb_total_isolated_cfdna = exact_lb_total_isolated_cfdna
    #     super().save(*args, **kwargs)

    # Section: Recruiter - 12 fields ###

    recruiting_site = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=SITE_CHOICES,
        verbose_name="Recruiting Site")

    patient_identifier = models.CharField(
        max_length=5,
        validators=[validators.validate_patient_identifier],
        verbose_name="Patient Identifier")

    sex = models.CharField(max_length=CHARFIELD_MAXLEN, choices=SEX_CHOICES,
                           verbose_name="Sex")

    died = models.DateField(null=True, blank=True, verbose_name="Died",
                            validators=[validators.check_date])

    saturn3_sample_code = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        validators=[validators.check_sat3_sample_code],
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
        validators=[validators.no_commas_allowed])

    sampling_date = models.DateField(verbose_name="Sampling Date",
                                     validators=[validators.check_date])
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
        choices=CORRESPONDING_ORGANOID_CHOICES)

    grading = models.CharField(max_length=CHARFIELD_MAXLEN, choices=GRADING,
                               verbose_name="Grading", blank=True,
                               null=True)

    # Section: TUM Pathology ###

    tissue_quality = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1, "Value between 1 and 5"),
                    MaxValueValidator(5, "Value between 1 and 5")],
        verbose_name="Tissue Quality"
        )

    tumor_cell_content = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0,
                                      "Percentage value between 0 and 100"),
                    MaxValueValidator(100,
                                      "Percentage value between 0 and 100")],
        verbose_name="Tumor Cell Content [%]")

    percent_avital_cells = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0,
                                      "Percentage value between 0 and 100"),
                    MaxValueValidator(100,
                                      "Percentage value between 0 and 100")],
        verbose_name="Avital Cells [%]")

    comment_tumor_cell_content = models.TextField(
        blank=True, null=True,
        verbose_name="Comment Tumor Cell Content",
        validators=[validators.no_commas_allowed])

    # Section: SPL ###
    spl_received = models.DateField(
        null=True, blank=True,
        validators=[validators.check_date],
        verbose_name="SPL Date Received")

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

    # Section: ScLab ###
    sclab_received = models.DateField(
        null=True, blank=True, verbose_name="ScLab Date Received",
        validators=[validators.check_date])

    sclab_extraction_date = (models.
                             DateField(null=True,
                                       blank=True,
                                       verbose_name="ScLab "
                                       "Extraction Date",
                                       validators=[validators.check_date]))

    sclab_nuclei_yield = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0,
                                      "Positive integers only")],
        verbose_name="ScLab Nuclei Yield")

    sclab_nuclei_size = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0, "Percentage value between 0 and 100"),
            MaxValueValidator(100, "Percentage value between 0 and 100")],
        verbose_name="ScLab Particles "
                     "Above 5 µm [%]")

    sclab_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                    blank=True, null=True,
                                    verbose_name="ScLab Status",
                                    choices=SCLAB_STATUS_CHOICES)

    sclab_sequencing_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                             blank=True, null=True,
                                             verbose_name="ScLab"
                                                          " Sequencing Type",
                                             choices=SCLAB_SEQUENCING_TYPES)

    sclab_sorting = models.BooleanField(choices=CORRESPONDING_ORGANOID_CHOICES,
                                        blank=True, null=True,
                                        verbose_name="ScLab Sorting")
    sclab_pool = models.CharField(
        null=True,
        blank=True,
        validators=[validators.sclab_pool_validator],
        verbose_name="ScLab Pool")

    rna_isle_id = models.CharField(
        null=True,
        blank=True,
        max_length=11,
        validators=[validators.check_eleven_figures],
        verbose_name="RNA ILSE ID")

    atac_isle_id = models.CharField(
        null=True,
        blank=True,
        max_length=11,
        validators=[validators.check_eleven_figures],
        verbose_name="ATAC ILSE ID")

    sclab_comment = models.TextField(max_length=CHARFIELD_MAXLEN,
                                     blank=True,
                                     null=True,
                                     verbose_name="ScLab Comment",
                                     validators=[validators.no_commas_allowed]
                                     )

    # Section: Spatial ###
    spatial_method = models.CharField(blank=True, null=True,
                                      verbose_name="Spatial Method",
                                      choices=SPATIAL_METHOD)

    spatial_status = models.CharField(blank=True, null=True,
                                      verbose_name="Spatial Status",
                                      choices=SPATIAL_STATUS)

    xenium_run_date = models.DateField(null=True,
                                       blank=True,
                                       verbose_name="Xenium Run Date",
                                       validators=[validators.check_date])

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
                                         validators=[validators.check_date],
                                         verbose_name="Merscope Run Date")

    merscope_run_id = models.CharField(
        max_length=200,
        blank=True, null=True,
        verbose_name="Merscope Run ID")

    merscope_panel_id = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name="Merscope Panel ID")

    dv_200 = models.IntegerField(
        blank=True, null=True,
        max_length=3,
        verbose_name="DV200",
        validators=[
            MinValueValidator(0, "Percentage value between 0 and 100"),
            MaxValueValidator(100, "Percentage value between 0 and 100")],
                              )

    spatial_comment = models.TextField(blank=True, null=True,
                                       verbose_name="Spatial Comment",
                                       validators=[(validators
                                                    .no_commas_allowed)])

    # Section: LB ###
    lb_analyte_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                       blank=True, null=True,
                                       verbose_name="LB Analyte Type",
                                       choices=LB_ANALYTE_TYPES)

    lb_panel_r1 = models.CharField(blank=True, null=True,
                                   verbose_name="LB Panel R1")

    lb_panel_r2 = models.CharField(blank=True, null=True,
                                   verbose_name="LB Panel R2")

    lb_sequencing_status = models.CharField(
        blank=True, null=True,
        verbose_name="LB Sequencing Status",
        choices=LB_SEQUENCING_STATUS_CHOICES)

    lb_received = models.DateField(null=True,
                                   blank=True, verbose_name="LB Date Received",
                                   validators=[validators.check_date])

    lb_sample_volume = models.DecimalField(
        null=True, blank=True,
        max_digits=4, decimal_places=1,
        validators=[MinValueValidator(0, "Positive decimals only")],
        verbose_name="LB Sample"
                     " Volume [ml]")

    lb_date_of_isolation = models.DateField(null=True,
                                            blank=True,
                                            verbose_name="LB Date "
                                                         "of Isolation",
                                            validators=[validators.check_date])

    lb_total_isolated_cfdna = \
        models.DecimalField(null=True, blank=True,
                            verbose_name="LB Total Isolated cfDNA [ng]",
                            max_digits=4, decimal_places=2,
                            validators=[
                                MinValueValidator(0, "Positive values only"),])

    lb_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                 blank=True, null=True,
                                 verbose_name="LB Status",
                                 choices=LB_STATUS_CHOICES)

    # Section: OmicsDatapaths ###

    request_execution_of = models.CharField(
        blank=True,
        null=True,
        verbose_name="Request Execution of"
    )

    cell_ranger_arc_run = models.CharField(
        blank=True,
        null=True,
        verbose_name="Cellranger-arc Run",
        # validators=[validators.check_date]
    )

    sc_analysis_status = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScAnalysis Status",
        # choices=SCANALYSIS_CHOICES
        )

    s3_bucket_status = models.BooleanField(
        choices=YES_NO_CHOICES,
        blank=True, null=True,
        verbose_name="S3 Bucket Status")

    scrna_r1 = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScRNA R1")

    scrna_r2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScRNA R2")

    scatac_r1 = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScATAC R1")

    scatac_r2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScATAC R2")

    scatac_i2 = models.CharField(
        blank=True,
        null=True,
        verbose_name="ScATAC I2")

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

    wgs_ref = models.CharField(blank=True,
                               null=True,
                               verbose_name="WGS Reference")

    # Timestamp ###

    created = models.DateTimeField(null=True, blank=True, auto_now_add=True,
                                   verbose_name="Created at")
