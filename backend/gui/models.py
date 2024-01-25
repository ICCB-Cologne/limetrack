from django.db import models
from django.core.exceptions import ValidationError


CHARFIELD_MAXLEN = 50

SITE_CHOICES = [
    ("Essen", "Essen"),
    ("Heidelberg", "Heidelberg"),
    ("Frankfurt", "Frankfurt"),
    ("Göttingen", "Göttingen"),
    ("Heidelberg", "Heidelberg"),
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
    ("Blood", "Blood")
]

GRADING = [
    ("G1", "G1"),
    ("G2", "G2"),
    ("G3", "G3")
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

SEX_CHOICES = {
    ("f", "f"),
    ("m", "m"),
    ("d", "d")
}


def validate_alphanumeric(value):
    char: str
    for char in value:
        if not char.isalnum():
            raise ValidationError("Only letters and numbers allowed")


def zero_to_a_hundred(value):
    if type(value) is not int and int(value) < 0 or int(value) > 100:
        raise ValidationError("Value between 0 and 100")

# Create your models here.


class HistopathologicalSample(models.Model):

    def generate_patient_id(self):
        return self.patient_identifier + self.recruiting_site

    # recruiter ###
    recruiting_site = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=SITE_CHOICES)
    patient_identifier = models.CharField(
        max_length=5,
        help_text="5-digit SATURN3 pseudonym \
              (by Treuhandstelle Freiburg)",
        validators=[validate_alphanumeric])  # set this to primary key?
    # patient = models.CharField( max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    sex = models.CharField(max_length=CHARFIELD_MAXLEN, choices=SEX_CHOICES)
    died = models.DateField(null=True, blank=True)
    # tissue_name = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    # used_in = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype
    saturn3_sample_code = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        verbose_name="SATURN3 Sample Code",
        help_text="S3 + Entity - \
            Patient Identifier - \
            Sampling Timepoint - \
            Tissue Type + Order Number - \
            Storage Format - Analyte Type \
            + Order Number")
    sampling_date = models.DateField()
    tissue_type = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=TISSUE_TYPES)
    type_of_intervention = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=INTERVENTION_TYPES)
    localisation = models.CharField(
        max_length=CHARFIELD_MAXLEN, choices=LOCALISATION_CHOICE)
    corresponding_organoid = models.BooleanField(
        help_text="generated from the same biopsy/tissue piece")
    grading = models.CharField(max_length=CHARFIELD_MAXLEN, choices=GRADING)
    # histology_subtype = models.CharField(max_length=CHARFIELD_MAXLEN)
    # skip for prototype

    # TUM Pathology ###
    tumor_cell_content = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True,
        validators=[zero_to_a_hundred])

    # SPL ###
    spl_received = models.DateField(
        null=True, blank=True, verbose_name="SPL received")
    spl_status = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True,
        choices=SPL_STATUS_CHOICES,
        verbose_name="SPL status")
    spl_sequencing_type = models.CharField(
        max_length=CHARFIELD_MAXLEN,
        blank=True,
        choices=SPL_SEQUENCING_TYPES,
        verbose_name="SPL sequencing type")

    # scLab ###
    sclab_received = models.DateField(
        null=True, blank=True, verbose_name="scLab received")
    sclab_extraction_date = models.DateField(null=True,
                                             blank=True,
                                             verbose_name="scLab \
                                                extraction date")
    sclab_nuclei_yield = models.IntegerField(null=True,
                                             blank=True,
                                             verbose_name="scLab nuclei yield")
    sclab_nuclei_size = models.IntegerField(null=True,
                                            blank=True,
                                            verbose_name="scLab nuclei\
                                                  size [µm]")
    sclab_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                    blank=True, verbose_name="scLab status")
    sclab_sequencing_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                             blank=True,
                                             verbose_name="scLab\
                                                  sequencing type")
    sclab_sorting = models.BooleanField(null=True,
                                        blank=True,
                                        verbose_name="scLab sorting")
    sclab_pool = models.IntegerField(null=True,
                                     blank=True, verbose_name="scLab pool")

    # LB ###
    lb_analyte_type = models.CharField(max_length=CHARFIELD_MAXLEN,
                                       blank=True,
                                       verbose_name="LB analyte type",
                                       choices=LB_ANALYTE_TYPES)
    lb_sampling_date = models.DateField(null=True,
                                        blank=True,
                                        verbose_name="LB sampling date")
    lb_received = models.DateField(null=True,
                                   blank=True, verbose_name="LB received")
    lb_sample_volume = models.IntegerField(null=True,
                                           blank=True,
                                           verbose_name="LB sample\
                                              volume [ml]")
    lb_date_of_isolation = models.DateField(null=True,
                                            blank=True,
                                            verbose_name="LB date\
                                                  of isolation")
    lb_total_isolated_cfdna = models.IntegerField(null=True,
                                                  blank=True,
                                                  verbose_name="LB total\
                                                      isolated cfDNA [ng]")

    lb_status = models.CharField(max_length=CHARFIELD_MAXLEN,
                                 blank=True,
                                 verbose_name="LB status",
                                 choices=LB_STATUS_CHOICES)
