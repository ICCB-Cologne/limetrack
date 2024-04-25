from django.test import TestCase
from backend.gui.models import HistopathologicalSample
from django.test import Client
# Create your tests here.

class CSVFileDataCreation(TestCase):
    
    def setUp(self):
        """
        This test takes the entries of the csv_file_init.csv
        as test data. This data is correct and includes no faulty entries. 
        """
        all_field_names = []
        all_fields = HistopathologicalSample._meta.get_fields()[1:]
        for field in all_fields:
            all_field_names.append(field.name)

        data1 = ["Frankfurt","3ri2d","f","2021-02-05","S3M-3ri2d-0-M1-Y-R1","2021-02-05",
                 "Fresh-Frozen","Resection","Pancreas","True","G1","12","2023-12-12","RNA failed",
                 "panel","2023-12-12","2023-12-12",None,"45","RNA failed","Multiome (RNA/ATAC)",
                 "True","44","123456","123456","LOL","CTC",None,"2023-12-12","8","2023-12-12",
                 "111","DNA failed",None,None,None,None,None,None,None,None,None,None]
        dict1 = dict(zip(all_field_names, data1))


        data2 = ["Frankfurt","11rt7","f",None,"S3C-11rt7-1-S1-V-R1","2021-02-06","FFPE","Blood withdrawal",
                 "Breast","False","G2","45","2023-12-13","DNA failed","WGS","2023-12-13","2023-12-13","99",
                 "45",None,"RNA","False",None,"123456","123456","LOL",None,"2023-12-12","2023-12-13","545",
                 None,"111","successful DNA",None,None,None,None,None,None,None,None,None,None]
        dict2 = dict(zip(all_field_names, data2))
        

        data3 = ["Göttingen","as231","m",None,"S3P-as231-0-M1-Y-R1","2021-02-07","Viable","Punctate","Colon",
                 "True","G3","48","2023-12-14",None,"WGS/RNA",None,None,"213","45","sequencing failed","ATAC",
                 "True","112","123456","123456","LOL","ctDNA","2023-12-13","2023-12-14","54","2023-12-14",None,
                 "sequencing failed","1","link1","link2","link3","link4","link5","link6","link7","link8","link9"]
        dict3 = dict(zip(all_field_names, data3))


        HistopathologicalSample.objects.create(**dict1)
        HistopathologicalSample.objects.create(**dict2)
        HistopathologicalSample.objects.create(**dict3)

    def test_humene(self):
        self.assertEqual("LOL", 'LOL')


class LoginTest(TestCase):

    def test_login(self):
        c = Client()
        response = c.post("/login/", {"user_name": "rosot", "password": "root"})
        print("post test_login")
        print(response.status_code)
        print(response.content)
        print("get test_login")
        response = c.get("/login/")
        #print(response.content)