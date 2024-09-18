# CLIF Project Template Repository

This repository provides a recommended structure for CLIF project repositories. The proposed layout promotes consistency, facilitates collaboration, and ensures that all essential components are included in each project. While this structure serves as a guideline, Principal Investigators (PIs) have the flexibility to modify it or add additional directories as needed to suit their project's specific requirements.

## Repository Structure

```
project-template/
├── .gitignore
├── README.md
├── LICENSE
├── environment.yml or requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── outputs/
├── docs/
│   ├── project_proposal.md
│   └── additional_docs/
├── notebooks/
│   ├── 1_data_qc.ipynb
│   ├── 2_cohort_identification.ipynb
│   └── 3_analysis.ipynb
├── scripts/
│   ├── qc/
│   ├── cohort_selection/
│   └── analysis/
├── src/
│   └── utils/
├── tests/
│   └── test_data_quality.py
└── CHANGELOG.md
```

### Description of Repository Components

- **`.gitignore`**: Specifies intentionally untracked files to ignore.
- **`README.md`**: Provides an overview of the project, setup instructions, and usage guidelines.
- **`LICENSE`**: Contains the licensing information for the project.
- **`environment.yml`** or **`requirements.txt`**: Lists all dependencies and packages required to run the project.

### `data/` Directory

- **`raw/`**: Placeholder for raw data files. *Note: Do not include actual data in the repository.*
- **`processed/`**: Stores processed data resulting from cleaning and transformation.
- **`outputs/`**: Contains analysis results such as figures and tables.

### `docs/` Directory

- **`project_proposal.md`**: Detailed project proposal outlining objectives, methodologies, and expected outcomes.
- **`additional_docs/`**: Additional documentation like meeting notes or supplementary materials.

### `notebooks/` Directory

- **`1_data_qc.ipynb`**: Jupyter notebook for data quality checks. This could also be a `.qmd` or `.Rmd` file. 
- **`2_cohort_identification.ipynb`**: Notebook for defining and identifying the cohort. This could also be a `.qmd` or `.Rmd` file. 
- **`3_analysis.ipynb`**: Notebook(s) for executing project-specific analyses. This could also be a `.qmd` or `.Rmd` file. 

### `scripts/` Directory

- **`qc/`**: Scripts related to data quality checks.
- **`cohort_selection/`**: Scripts for cohort identification processes.
- **`analysis/`**: Scripts for data analysis tasks.

### `src/` Directory

- **`utils/`**: Utility functions and modules used throughout the project.

### `tests/` Directory

- **`test_data_quality.py`**: Unit tests for verifying data quality functions.

### Other Files

- **`CHANGELOG.md`**: Records all notable changes made to the project to facilitate tracking of progress and updates.

---

By following this template, project teams can ensure a well-organized repository that supports efficient collaboration and effective project management. Feel free to adjust the structure to better fit your project's needs.

