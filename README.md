# CLIF Project Title

## Objective

Describe the project objective

## Required CLIF tables and fields

Please refer to the online [CLIF data dictionary](https://clif-consortium.github.io/website/data-dictionary.html), [ETL tools](https://github.com/clif-consortium/CLIF/tree/main/etl-to-clif-resources), and [specific table contacts](https://github.com/clif-consortium/CLIF?tab=readme-ov-file#relational-clif) for more information on constructing the required tables and fields. List all required tables for the project here, and provide a brief rationale for why they are required.

## Cohort identification
Describe study cohort inclusion and exclusion criteria here

## Project Environment
Describe the steps to setup the project environment and other configurations

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
- **`.renv`** or **`requirements.txt`**: Lists all dependencies and packages required to run the project.
- **`outputs/` Directory**: Contains analysis results such as figures and tables.
- **`code/` Directory**: Contains code as R/Python scripts or .Rmd/.qmd/jupyter notebooks.  The code is broadly related to data quality checks, cohort identification processes and data analysis tasks
- **`utils/` Directory**: Utility functions and modules used throughout the project. Some common utility functions for CLIF projects are provided.

## Example Repositories
* [CLIF Adult Sepsis Events](https://github.com/08wparker/CLIF_adult_sepsis_events) for R
* [CLIF Eligibility for mobilization](https://github.com/kaveriC/mobilization) for Python
---


