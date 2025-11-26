# NYPD Reported Crime Interactive Dashboard
---
## Project Description

An interactive dashboard web app on the crime rate in New york since 2006

## Dataset Location
- https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i

___

## Project Structure(src/)
- ### .streamlit/
    -  app layout and theme configuration files
- ### data/
    - `NYPD_ComplaintDataHistoric.csv`[^note]
    - `data_subset.csv`[^note]
    - `pipeline.py` - run this to create data_subset.csv
- ### pages/
    - `about.py` - Information Page

- ### Dashboard.py
    - web app home page
- ### style.css
    - more detailed styling for webapp elements

- ### environment.yml
    - anaconda package list to replicate environment

[^note]: File not included

---

## How to Run Locally
- Download this repo
- Install anaconda and pip packages from `environment.yml` (in a virtual environment)
- Download the [dataset](#dataset-location) into `data\` directory
- Run the following to copy the columns needed into a new csv `data_subset.csv`:
  `python3 data\pipeline.py`
- Run the following to launch the app:
  `streamlit run Dashboard.py`