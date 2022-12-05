# NYPD Reported Crime Interactive Dashboard
---
## Project Description

An interactive dashboard web app on the crime rate in New york since 2006

## Dataset Located at
- https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i

___

## Project Structure
- ### requirements/
    > pip and conda requirements
- ### .streamlit/
    > app layout and theme configuration files
- ### data/
    > `NYPD_ComplaintDataHistoric.csv`[^note]\
    > `data_subset.csv`[^note]\
    > `transform.py` - run this create data_subset.csv
- ### pages/
    > about.py - Information Page

- ### `Dashboard.py`
    - web app home
- ### `style.css`
    - more detailed styling for webapp elements

[^note]: File not included

---

## How to Run Locally
- Download this repo
- Create new Conda environment
- Install packages from requirements folder
- Go to terminal/command line and run the following command in root directory :
  `streamlit run Dashboard.py`