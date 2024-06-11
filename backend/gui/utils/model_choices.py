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
    ("Spleen", "Spleen"),
    ("Skin", "Skin"),
]

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

SPATIAL_METHOD = [
    ("Xenium", "Xenium"),
    ("Merscope", "Merscope"),
    ("Xenium/Merscope", "Xenium/Merscope"),
]

SPATIAL_STATUS = [
    ("Xenium failed", "Xenium failed"),
    ("Merscope failed", "Merscope failed"),
    ("successful Xenium", "successful Xenium"),
    ("successful Merscope", "successful Merscope"),
    ("failed Xenium/Merscope", "failed Xenium/Merscope"),
]
