from backend.gui.utils.model_choices import (LOCALISATION_CHOICE, SITE_CHOICES,
                                             SEX_CHOICES,
                                             TISSUE_TYPES, INTERVENTION_TYPES,
                                             CORRESPONDING_ORGANOID_CHOICES,
                                             GRADING,
                                             SPL_SEQUENCING_TYPES,
                                             SPL_STATUS_CHOICES,
                                             SCLAB_SEQUENCING_TYPES,
                                             SCLAB_STATUS_CHOICES,
                                             LB_ANALYTE_TYPES,
                                             LB_STATUS_CHOICES)

import random


class RecordGenerator:

    @staticmethod
    def generate_localisation():
        return random.choice(LOCALISATION_CHOICE)
