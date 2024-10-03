# CLIF Project Template

This repository provides a recommended structure for CLIF project repositories. The proposed layout promotes consistency, facilitates collaboration, and ensures that all essential components are included in each project. While this structure serves as a guideline, Principal Investigators (PIs) have the flexibility to modify it or add additional directories as needed to suit their project's specific requirements.

## Repository Structure

```
project-template/
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt or .renv
├── config/
├── outputs/
├── outlier-thresholds/
├── code/
├── utils/
```

### Description of Repository Components

- **`.gitignore`**: Specifies intentionally untracked files to ignore.
- **`README.md`**: Provides an overview of the project, setup instructions, and usage guidelines.
- **`LICENSE`**: Contains the licensing information for the project.
- **`environment.yml`** or **`requirements.txt`**: Lists all dependencies and packages required to run the project.
- **`outputs/` Directory**: Contains analysis results such as figures and tables.
- **`code/` Directory**: Contains code as R/Python scripts or .Rmd/.qmd/jupyter notebooks.  The code is broadly related to data quality checks, cohort identification processes and data analysis tasks
- **`utils/` Directory**: Utility functions and modules used throughout the project. Some common utility functions for CLIF projects are provided.

---

# CLIF Project Title

## Objective

Describe the project objective

## Required CLIF tables and fields

Please refer to the online CLIF data dictionary, ETL tools, and specific table contacts for more information on constructing the required tables and fields.
List all required tables for the project here, and provide a brief rationale for why they are required.
For more advanced tables, indicate if the entire table is required, only specific fields, or only a filtered version.

## Cohort identification
Describe study cohort inclusion and exclusion criteria here

## Project Environment
Describe the steps to setup the project environment and other configurations
