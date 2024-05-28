from django.db import models
from django.core.exceptions import ValidationError
import re

CHARFIELD_MAXLEN = 200

SITE_CHOICES = [
    ("Essen", "Essen"),
    ("Heidelberg", "Heidelberg"),
    ("Frankfurt", "Frankfurt"),
    ("Göttingen", "Göttingen"),
    ("Köln", "Köln"),
    ("München", "München"),
    ("Augsburg", "Augsburg")
]

TISSUE_TYPES = [
    ("Fresh-Frozen", "Fresh-Frozen"),
    ("FFPE", "FFPE"),
    ("Viable", "Viable"),
    ("Pleurapunctate", "Pleurapunctate"),
    ("Ascites", "Ascites"),
    ("CTC", "CTC"),
    ("PBMC", "PBMC"),
    ("Serum", "Serum"),
    ("Plasma", "Plasma"),
    ("ctDNA", "ctDNA"),
    ("Whole blood", "Whole blood"),
    ("Organoid", "Organoid")
]

INTERVENTION_TYPES = [
    ("Resection", "Resection"),
    ("Biopsy", "Biopsy"),
    ("Blood withdrawal", "Blood withdrawal"),
    ("Punctate", "Punctate")
]

LOCALISATION_CHOICE = [
    ("Pancreas", "Pancreas"),
    ("Breast", "Breast"),
    ("Colon", "Colon"),
    ("Liver", "Liver"),
    ("Brain", "Brain"),
    ("Lung", "Lung"),
    ("Thorax Wall", "Thorax Wall"),
    ("Pleura Punctate", "Pleura Punctate"),
    ("Ascites", "Ascites"),
    ("Blood", "Blood"),
    ("Peritoneum", "Peritoneum"),
    ("Lymph Node", "Lymph Node"),
    ("Spleen", "Spleen")
]

GRADING = [
    ("G1", "G1"),
    ("G2", "G2"),
    ("G3", "G3")
]

SCLAB_STATUS_CHOICES = [
    ("RNA failed", "RNA failed"),
    ("ATAC failed", "ATAC failed"),
    ("sequencing failed", "sequencing failed"),
    ("ATAC/RNA failed", "ATAC/RNA failed"),
    ("successful RNA", "successful RNA"),
    ("successful ATAC", "successful ATAC"),
    ("successful ATAC/RNA", "successful ATAC/RNA")
]

SPL_STATUS_CHOICES = [
    ("RNA failed", "RNA failed"),
    ("DNA failed", "DNA failed"),
    ("sequencing failed", "sequencing failed"),
    ("DNA/RNA failed", "DNA/RNA failed"),
    ("successful RNA", "successful RNA"),
    ("successful DNA", "successful DNA"),
    ("successful DNA/RNA", "successful DNA/RNA")
]

SPL_SEQUENCING_TYPES = [
    ("panel", "panel"),
    ("WGS", "WGS"),
    ("WGS/RNA", "WGS/RNA"),
    ("WES", "WES"),
    ("WES/RNA", "WES/RNA")
]

SCLAB_SEQUENCING_TYPES = [
    ("Multiome (RNA/ATAC)", "Multiome (RNA/ATAC)"),
    ("RNA", "RNA"),
    ("ATAC", "ATAC"),
]

LB_ANALYTE_TYPES = [
    ("Plasma", "Plasma"),
    ("CTC", "CTC"),
    ("ctDNA", "ctDNA"),
    ("PBMC", "PBMC"),
    ("Serum", "Serum")
]

LB_STATUS_CHOICES = [
    ("DNA failed", "DNA failed"),
    ("successful DNA", "successful DNA"),
    ("sequencing failed", "sequencing failed"),
    ("sequencing successful", "sequencing successful"),
]

SEX_CHOICES = [
    ("f", "f"),
    ("m", "m")
]

CORRESPONDING_ORGANOID_CHOICES = [
    (True, "Yes"),
    (False, "No"),
]


def validate_alphanumeric(value):
    char: str
    if len(value) < 5:
        raise ValidationError("Lenght has to be exactly 5 characters")
    for char in value:
        if not char.isalnum():
            raise ValidationError("Only letters and numbers allowed")


def zero_to_a_hundred(value):
    if type(value) is not int:
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

    Meaning go to forms.py and make sure
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
