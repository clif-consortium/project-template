import sys
import os

# Add the parent directory of the current script to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import the config module from utils
from utils import config

# Use the imported config
# For example, access a configuration value
site_name = config['site_name']

# Your cohort identification code here
# Cohort identification script for inpatient admissions

# Load required libraries
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import pyarrow.parquet as pq
import pyarrow.dataset as ds
from pyarrow import csv
import fst
from tableone import TableOne

# Objective: identify a cohort of hospitalizations from CLIF tables
# Identify patients admitted to the hospital in a given date range. 
# Export a list of `hospitalization_id` and filtered CLIF tables for the 
# identified hospitalizations.
# An example project for this cohort would be included for surveillance of 
# sepsis events based on the CDC Adult Sepsis Event criteria.

# Specify inpatient cohort parameters

## Date range
start_date = "2020-01-01"
end_date = "2021-12-31"

## Inclusion and exclusion criteria
include_pediatric = False
include_er_deaths = True

# TO DO: develop these criteria further

# Specify required CLIF tables

# List of all table names from the CLIF 2.0 ERD
tables = ["patient", "hospitalization", "vitals", "labs", 
          "medication_admin_continuous", "adt", "patient_assessments",
          "respiratory_support", "position", "dialysis", "intake_output", 
          "ecmo_mcs", "procedures", "admission_diagnosis", "provider", 
          "sensitivity", "medication_orders", "medication_admin_intermittent",
          "therapy_details", "microbiology_culture", "sensitivity", 
          "microbiology_nonculture"]

# Tables that should be set to TRUE for this project
true_tables = ["patient", "hospitalization", "adt", "microbiology_culture", 
               "vitals", "labs", "medication_admin_continuous", 
               "respiratory_support"]

# Create a dictionary and set the boolean values
table_flags = {table: table in true_tables for table in tables}

# Load the required CLIF tables into memory and return an error if a required 
# table is missing

## Specify CLIF table location in your repository

# Access configuration parameters
site_name = config['site_name']
tables_path = config['tables_path']
file_type = config['file_type']

# Print the configuration parameters
print(f"Site Name: {site_name}")
print(f"Tables Path: {tables_path}")
print(f"File Type: {file_type}")

# List all CLIF files in the directory
clif_table_filenames = list(Path(tables_path).glob(f"clif_*.{file_type}"))

# Extract the base names of the files (without extension)
clif_table_basenames = [f.stem for f in clif_table_filenames]

# Create a lookup table for required files based on table_flags
required_files = [f"clif_{table}" for table, flag in table_flags.items() if flag]

# Check if all required files are present
missing_tables = set(required_files) - set(clif_table_basenames)
if missing_tables:
    raise Exception(f"Missing required tables: {', '.join(missing_tables)}")

# Filter only the filenames that are required
required_filenames = [f for f in clif_table_filenames if f.stem in required_files]

# Read the required files into a dictionary of dataframes
data_dict = {}
if file_type == "parquet":
    for file in required_filenames:
        dataset = ds.dataset(file, format="parquet")
        data_dict[file.stem] = dataset.to_table().to_pandas()
        # Apply your filter condition here if needed
elif file_type == "csv":
    for file in required_filenames:
        data_dict[file.stem] = pd.read_csv(file)
elif file_type == "fst":
    for file in required_filenames:
        data_dict[file.stem] = fst.read_fst(file)
else:
    raise Exception("Unsupported file format")

# Assign the dataframes to variables based on their file names
for object_name, df in data_dict.items():
    globals()[object_name] = df

del data_dict

# Identify hospital admissions for the specified date range with at least one
# `location_category` of `c("Ward", "ICU")`

clif_hospitalization_filtered = clif_hospitalization[
    (clif_hospitalization['admission_dttm'] >= start_date) & 
    (clif_hospitalization['admission_dttm'] <= end_date)
]

if not include_pediatric:
    clif_hospitalization_filtered = clif_hospitalization_filtered[
        clif_hospitalization_filtered['age_at_admission'] >= 18
    ]

inpatient_hospitalization_ids = clif_adt[
    clif_adt['location_category'].isin(['Ward', 'ICU'])
]['hospitalization_id'].unique()

cohort_hospitalization_ids = clif_hospitalization_filtered[
    clif_hospitalization_filtered['hospitalization_id'].isin(inpatient_hospitalization_ids)
]['hospitalization_id'].unique()

## Identify patients who died in the ER and include if specified

if include_er_deaths:
    # identify hospitalization_ids with only ER location_category
    ER_only_hospitalization_ids = clif_adt.groupby('hospitalization_id').filter(
        lambda x: (x['location_category'] == 'ER').all()
    )['hospitalization_id'].unique()

    ER_death_ids = clif_hospitalization[
        (clif_hospitalization['hospitalization_id'].isin(ER_only_hospitalization_ids)) &
        (clif_hospitalization['discharge_category'] == 'Expired')
    ]['hospitalization_id'].unique()

    cohort_hospitalization_ids = np.union1d(cohort_hospitalization_ids, ER_death_ids)

## Export the list of `hospitalization_id` for the identified patients

np.save(Path(cohort_path) / "cohort_hospitalization_ids.npy", cohort_hospitalization_ids)

## Filter the CLIF tables for the identified hospitalizations

def filter_clif_table(table, filter_col, cohort_ids, select_cols=None):
    filtered_table = table[table[filter_col].isin(cohort_ids)]
    
    # Optionally select relevant columns
    if select_cols is not None:
        filtered_table = filtered_table[select_cols]
    
    return filtered_table

# Remove the patient table from the list of tables to filter
table_flags['patient'] = False

# Filter the required tables for the identified hospitalizations
for table_name, flag in table_flags.items():
    if flag:
        full_table_name = f"clif_{table_name}"
        globals()[f"{full_table_name}_cohort"] = filter_clif_table(
            globals()[full_table_name], 
            "hospitalization_id", 
            cohort_hospitalization_ids
        )

# Filter the patient table for the identified patients
cohort_patient_ids = clif_hospitalization_cohort['patient_id'].unique()

clif_patient_cohort = filter_clif_table(clif_patient, "patient_id", cohort_patient_ids)

# TO DO:
# - drop unecessary fields or observations in this step as well, e.g. filter 
#   `labs` down to only the labs that are relevant for the sepsis surveillance 
#   project.
# - convert to a shiny app

## Save all filtered tables to the `study_cohort` folder

cohort_tables = {name: value for name, value in globals().items() if name.startswith('clif_') and name.endswith('_cohort')}
pd.to_pickle(cohort_tables, Path(cohort_path) / "clif_cohort_tables.pkl")

# Create a table 1 of patient demographics for the cohort

admits_per_patient = clif_hospitalization_cohort.groupby('patient_id').size().reset_index(name='n_hospitalizations')

table_one_patient = clif_patient_cohort.merge(admits_per_patient, on='patient_id', how='left')
table_one_patient['age'] = (pd.to_datetime(start_date) - pd.to_datetime(table_one_patient['birth_date'])).dt.days / 365.25

columns = ['age', 'sex_category', 'race_category', 'ethnicity_category', 'n_hospitalizations', 'language_name']
table_one_patient = TableOne(table_one_patient, columns=columns)

print(table_one_patient)

# Create table 1 of hospitalization level data for the cohort

ever_icu = clif_adt_cohort[clif_adt_cohort['location_category'] == 'ICU']['hospitalization_id'].unique()
ever_icu = pd.DataFrame({'hospitalization_id': ever_icu, 'ever_icu': 1})

table_one_hospitalization = clif_hospitalization_cohort.copy()
table_one_hospitalization['length_of_stay'] = (pd.to_datetime(table_one_hospitalization['discharge_dttm']) - 
                                               pd.to_datetime(table_one_hospitalization['admission_dttm'])).dt.days

table_one_hospitalization = table_one_hospitalization.merge(
    clif_patient_cohort[['patient_id', 'race_category', 'sex_category', 'ethnicity_category', 'language_name']],
    on='patient_id',
    how='left'
)

table_one_hospitalization = table_one_hospitalization.merge(ever_icu, on='hospitalization_id', how='left')
table_one_hospitalization['ever_icu'] = table_one_hospitalization['ever_icu'].fillna(0)

columns = ['age_at_admission', 'discharge_category', 'admission_type_name', 'length_of_stay',
           'race_category', 'sex_category', 'ethnicity_category', 'language_name']
groupby = ['ever_icu']

table_one_hospitalization = TableOne(table_one_hospitalization, columns=columns, groupby=groupby)

# Export the table
table_one_hospitalization.to_csv(Path("results") / f"Table_One_{datetime.now().date()}_{config['site_name']}.csv")
