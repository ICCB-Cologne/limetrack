LOCALISATION_CHOICE = [
    ("Adrenal gland", "Adrenal gland"),
    ("Ascites", "Ascites"),
    ("Blood", "Blood"),
    ("Brain", "Brain"),
    ("Breast", "Breast"),
    ("Colon", "Colon"),
    ("Diaphragm", "Diaphragm"),
    ("Liver", "Liver"),
    ("Lung", "Lung"),
    ("Lymph node", "Lymph node"),
    ("Ovary", "Ovary"),
    ("Pancreas body", "Pancreas body"),
    ("Pancreas head", "Pancreas head"),
    ("Pancreas tail", "Pancreas tail"),
    ("Pericardium", "Pericardium"),
    ("Peripancreatic fat", "Peripancreatic fat"),
    ("Peritoneum", "Peritoneum"),
    ("Pleura punctate", "Pleura punctate"),
    ("Skin", "Skin"),
    ("Spleen", "Spleen"),
    ("Thorax wall", "Thorax wall"),
    ("Visceral fat", "Visceral fat"),
]

SITE_CHOICES = [
    ("Augsburg", "Augsburg"),
    ("Essen", "Essen"),
    ("Frankfurt", "Frankfurt"),
    ("Göttingen", "Göttingen"),
    ("Heidelberg", "Heidelberg"),
    ("Köln", "Köln"),
    ("München", "München"),
]

TISSUE_TYPES = [
    ("Ascites", "Ascites"),
    ("Buffy coat", "Buffy coat"),
    ("CTC", "CTC"),
    ("ctDNA", "ctDNA"),
    ("FFPE", "FFPE"),
    ("Fresh-Frozen", "Fresh-Frozen"),
    ("Organoid", "Organoid"),
    ("PBMC", "PBMC"),
    ("Plasma", "Plasma"),
    ("Pleurapunctate", "Pleurapunctate"),
    ("Serum", "Serum"),
    ("Viable", "Viable"),
    ("Whole blood", "Whole blood"),
]

INTERVENTION_TYPES = [
    ("Autopsy", "Autopsy"),
    ("Biopsy", "Biopsy"),
    ("Blood withdrawal", "Blood withdrawal"),
    ("Punctate", "Punctate"),
    ("Resection", "Resection"),
]

GRADING = [
    ("G1", "G1"),
    ("G2", "G2"),
    ("G3", "G3")
]

SCLAB_STATUS_CHOICES = [
    ("successful ATAC", "successful ATAC"),
    ("successful RNA", "successful RNA"),
    ("successful ATAC/RNA", "successful ATAC/RNA"),
    ("ATAC failed", "ATAC failed"),
    ("RNA failed", "RNA failed"),
    ("ATAC/RNA failed", "ATAC/RNA failed"),
    ("sequencing failed", "sequencing failed"),
]

SPL_STATUS_CHOICES = [
    ("successful DNA", "successful DNA"),
    ("successful RNA", "successful RNA"),
    ("successful DNA/RNA", "successful DNA/RNA"),
    ("DNA failed", "DNA failed"),
    ("RNA failed", "RNA failed"),
    ("DNA/RNA failed", "DNA/RNA failed"),
    ("sequencing failed", "sequencing failed"),
]

SPL_SEQUENCING_TYPES = [
    ("Panel", "Panel"),
    ("SNParray", "SNParray"),
    ("WES", "WES"),
    ("WES/RNA", "WES/RNA"),
    ("WGS", "WGS"),
    ("WGS/RNA", "WGS/RNA"),
]

SCLAB_SEQUENCING_TYPES = [
    ("ATAC", "ATAC"),
    ("RNA", "RNA"),
    ("Multiome (RNA/ATAC)", "Multiome (RNA/ATAC)"),
]

LB_ANALYTE_TYPES = [
    ("CTC", "CTC"),
    ("ctDNA", "ctDNA"),
    ("PBMC", "PBMC"),
    ("Plasma", "Plasma"),
    ("Serum", "Serum")
]

LB_STATUS_CHOICES = [
    ("successful DNA", "successful DNA"),
    ("sequencing successful", "sequencing successful"),
    ("DNA failed", "DNA failed"),
    ("sequencing failed", "sequencing failed"),
]

LB_SEQUENCING_STATUS_CHOICES = [
    ("Panel", "Panel"),
    ("sWGS", "sWGS"),
    ("sWGS & Panel", "sWGS & Panel")
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
    ("C", "C"),
    ("F", "F"),
    ("L", "L"),
    ("M", "M"),
    ("N", "N"),
    ("R", "R"),
    ("T", "T"),
    ("X", "X"),
]

STORAGE_FORMAT = [
    ("F", "F"),
    ("O", "O"),
    ("P", "P"),
    ("S", "S"),
    ("V", "V"),
    ("Y", "Y"),
    ]

ANALYTE_TYPE = [
    ("C", "C"),
    ("D", "D"),
    ("G", "G"),
    ("H", "H"),
    ("L", "L"),
    ("M", "M"),
    ("N", "N"),
    ("R", "R"),
    ("T", "T"),
    ("W", "W"),
    ("Y", "Y"),
]

SPATIAL_METHOD = [
    ("Xenium", "Xenium"),
    ("Merscope", "Merscope"),
    ("Xenium/Merscope", "Xenium/Merscope"),
]

SPATIAL_STATUS = [
    ("successful Merscope", "successful Merscope"),
    ("successful Xenium", "successful Xenium"),
    ("successful Xenium/Merscope", "successful Xenium/Merscope"),
    ("Xenium failed", "Xenium failed"),
    ("Merscope failed", "Merscope failed"),
    ("failed Xenium/Merscope", "failed Xenium/Merscope"),

]

SCANALYSIS_CHOICES = [
    ("count files", "count files"),
    ("demultiplexed", "demultiplexed"),
    ("demultiplexed + QC", "demultiplexed + QC")
]
