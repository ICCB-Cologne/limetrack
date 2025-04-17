# LiMeTrack - A lightweight biosample management platform
**LiMeTrack** is a lightweight biosample management platform for centralized research data management and sample tracking in biomedical research projects.

Key features include customizable and user-friendly forms for data entry and a real-time dashboard providing an overview of project and sample status. 
LiMeTrack simplifies the creation and export of standardized sample sheets, streamlining subsequent bioinformatics analyses and biomedical research workflows. 
By integrating real-time monitoring with robust sample tracking and data management, LiMeTrack improves research transparency and reproducibility, ensures data integrity and optimizes workflows.

Users can submit data either by filling out a web form or uploading CSV/Excel files.  
Accepted data is displayed as records in a filterable and searchable sample table.  

**LiMeTrack** is currently designed for the multicenter SATURN3 consortium (saturn3.org).
To meet the requirements of other projects, code and data model need to be adapted.
We are working on further simplifying the data models to be modularly adaptable for a wide range of projects.

## Prerequisites
Docker, Knowledge of Django & Python 

## Use your own data model
To apply your own data model to **LiMeTrack** you will need to modify the code 
in several ways:

### Define model fields, permissions & validators
The **LiMeTrack** code is built on dealing with a single django data model.  
You can define the data fields for your model in `backend/gui/model.py`.  
In our use case we defined a single model divided into multiple "sections"  
to manage user permissions (`end_of_model_section_dict` & `permissions`)

Users can get permissions to
1) **fill in** empty fields of specified sections
2) **edit already** filled fields of specified sections
3) **add** new records
4) **delete** existing records

Model specific permissions are defined inside the model class.

### Modify model form
In the frontend, our single model is represented by a single form.  
It is defined in `backend/gui/forms/forms.py`.  
The module `backend/gui/utils/model_to_form.py` helps transforming the concept of our  
single model with different sections into a corresponding form with the correct behaviour.  
Our approach here is to show each user the complete form, including all its form fields.  
However,
- Fields that are not to be filled or edited by the user are disabled and grayed out.
- An exception in our case are the omics fields,
that are only displayed to users with permissions to fill or edit them.

### Modify template & example files
In `backend/gui/views/download_views-py` you will find `example_sample`, a list that  
serves as mock sample to give an idea on how a complete sample should look like.  
The `csv-files/` directory contains csv-files (and xlsx-files) with example samples for file uploads.  
When changing the model, update the template & example samples accordingly.  

### Adapt column filters for the samples table
Column filters are defined as a form in `backend/gui/forms/forms.py`.  
They are meant to improve the overview of the samples table by displaying only  
selected fields/columns.  
The actual filtering logic is handled in `backend/gui/views/samples_view.py`.  
Data field lists are defined here to specify which columns should be displayed for
- every data model section
- different groups of data fields that are relevant 

### Modify selenium test cases
For basic integration tests we use Selenium to simulate user input (via web form and file upload).  
Especially the web form inputs have to be adapted to a new model.  
These tests can be found in `backend/gui/selenium/`.

### More information
For more detailed information, please refer to the documentation within the code.

## Docker Setup

### For local development and debugging

`docker compose -f docker-compose-local.yml -f docker-compose-develop.yml up --remove-orphans`

### Productive environment - Clean Volume On Reboot

`docker compose -f docker-compose.yml -f docker-compose-develop.yml up --remove-orphans --force-recreate`

### Productive environment Persist Volumes On Reboot

`docker compose -f docker-compose.yml -f docker-compose-develop.yml up --remove-orphans`

