## Change Log

---
### 2024-12-18

- **New**
    - Added Sign Up with Google Forms link on login page
    - New user Liquid_HD with special permissions
- **Updated Liquid Biopsy data fields**
    - 3 fields added: *LB Panel R1*, *LB Panel R2*, *LB Sequencing Status*
    - 1 field removed: *LB Sampling Date*
    - 1 field modified: *LB Sample Volume* data type changed to decimal number with max 4 digits and 1 decimal number.
- **Updated OMICS data fields**
    - 2 fields added: *Request Execution of*, *Cellranger-arc run*
- **Updated Recruiter data fields**
    - 2 fields modified: *Type of Intervention* has a new option in its dropdown field: "Autopsy", *Localisation* has a new option in its dropdown field: "Pancreatic fat"
- **Sample table**
    - Rearranged OMICS columns when filtering out all other groups.
    - Date format reset to YYYY-MM-DD (international)
- **Bug fixes**
    - Issue with filtered table download resolved.
---

### 2024-12-06

- **Housekeeping:**
    - Implemented [gunicorn](https://gunicorn.org/) to be used instead of django default server
    - Cleaned up Django templates 
- **Sample table:**
    - Rearranged ODCF's "ScAnalysis status" column to the left
- **Form input confirmation**
    - If a user types in wrong data types, the form now asks the user to correct their input before displaying the data confirmation view
---

### 2024-10-01

- **New:**
    - Added bulk upload for users
---

### 2024-09-25

- **New:**
    - Sample table: The downloaded files retain the filter settings and therefore contain only the previously filtered data
    - Dashboard: Mapplot type changed
    - Read-only users
- **Bug fixes:**
    - Removed initial values from disabled fields
---

### 2024-09-06

- **New:**
    - Sample table: Limited both visible string size and overall width of the columns.
    - Input restriction for comment and note fields: Commas are prohibited now.
    - Dashboard: Sample processing plot now also displays the percentage of samples in WGS.
---

### 2024-08-13

- **New:**
    - Added FAQ regarding the structure of the SATURN3 sample code
    - Files can now also be imported formatted in MS Excel
- **User Requests:**
    - TUM can now edit fields formerly reserved for SPL
- **Housekeeping:**
    - Security Updates

---

### 2024-08-07

- **New:** Entity filters for *SATURN3 Sample Code* column
- **Modification following user request:** Possible input values for the field *Tissue Quality* (TUM group) were restricted to 0-5

---

### 2024-07-23

- Added FAQs
- Added Dashboard
- Added a home landingpage
    - Added this Changelog
    - Added links with project ressources
- *SPL Sequencing Type* renamed to *SPL Analysis Type*
- *SNParray* added to sequencing type choices
- *scAnalysis status* added to model
---