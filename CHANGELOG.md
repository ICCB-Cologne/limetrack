## Change Log

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