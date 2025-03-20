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
                                             LB_STATUS_CHOICES,
                                             SPATIAL_METHOD,
                                             SPATIAL_STATUS,
                                             SCANALYSIS_CHOICES,
                                             LB_SEQUENCING_STATUS_CHOICES)

from backend.gui.utils.model_choices import (ENTITY, TISSUE_TYPE,
                                             STORAGE_FORMAT,
                                             ANALYTE_TYPE)

import random
import string
import time
import decimal
import datetime


class RecordGenerator:

    @staticmethod
    def random_localisation():
        return random.choice(LOCALISATION_CHOICE)[0]

    @staticmethod
    def random_site_choice():
        return random.choice(SITE_CHOICES)[0]

    @staticmethod
    def random_sex_choice():
        return random.choice(SEX_CHOICES)[0]

    @staticmethod
    def random_tissue_type():
        return random.choice(TISSUE_TYPES)[0]

    @staticmethod
    def random_intervention_type():
        return random.choice(INTERVENTION_TYPES)[0]

    @staticmethod
    def random_corresponding_organoid_choice():
        return random.choice(CORRESPONDING_ORGANOID_CHOICES)[1]

    @staticmethod
    def random_grading():
        return random.choice(GRADING)[0]

    @staticmethod
    def random_spl_sequencing_types():
        return random.choice(SPL_SEQUENCING_TYPES)[0]

    @staticmethod
    def random_spl_status_choice():
        return random.choice(SPL_STATUS_CHOICES)[0]

    @staticmethod
    def random_sclab_sequencing_types():
        return random.choice(SCLAB_SEQUENCING_TYPES)[0]

    @staticmethod
    def random_sclab_status_choice():
        return random.choice(SCLAB_STATUS_CHOICES)[0]

    @staticmethod
    def random_sclab_sorting():
        return random.choice(CORRESPONDING_ORGANOID_CHOICES)[1]

    @staticmethod
    def random_spatial_method():
        return random.choice(SPATIAL_METHOD)[1]

    @staticmethod
    def random_spatial_status():
        return random.choice(SPATIAL_STATUS)[1]

    @staticmethod
    def random_lb_analyte_types():
        return random.choice(LB_ANALYTE_TYPES)[0]

    @staticmethod
    def random_lb_status_choice():
        return random.choice(LB_STATUS_CHOICES)[0]

    @staticmethod
    def random_patient_identifier():
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=5))

    @staticmethod
    def random_string_of_length(k):
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=k))

    @staticmethod
    def random_sample_code_number():
        return ''.join(random.choices(
            string.digits, k=1))

    @staticmethod
    def random_sample_code_entity_choice():
        return random.choice(ENTITY)[0]

    @staticmethod
    def random_sample_code_tissue_type():
        return random.choice(TISSUE_TYPE)[0]

    @staticmethod
    def random_storage_format():
        return random.choice(STORAGE_FORMAT)[0]

    @staticmethod
    def random_scanalysis_choice():
        return random.choice(SCANALYSIS_CHOICES)[0]

    @staticmethod
    def random_sample_code_analyte_type():
        return random.choice(ANALYTE_TYPE)[0]

    @staticmethod
    def random_spl_status():
        return random.choice(SPL_STATUS_CHOICES)[0]

    @staticmethod
    def random_spl_sequencing():
        return random.choice(SPL_SEQUENCING_TYPES)[0]

    @staticmethod
    def random_date():
        rand = random.uniform(0.0, 1.0)

        start = str(datetime.date(1900, 1, 1))
        end = str(datetime.date(3000, 1, 1))
        time_format = "%Y-%m-%d"
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))

        ptime = stime + rand * (etime - stime)

        return time.strftime(time_format, time.localtime(ptime))

    @staticmethod
    def random_integer_from_0_to_100():
        return str(random.choice(range(0, 101)))

    @staticmethod
    def random_decimal_4_digits_1_decimal():
        return str(decimal.Decimal(random.randrange(0, 9999))/10)

    @staticmethod
    def random_integer_from_1_to_5():
        return str(random.choice(range(1, 6)))

    @staticmethod
    def random_lb_sequencing_status():
        return random.choice(LB_SEQUENCING_STATUS_CHOICES)[0]
