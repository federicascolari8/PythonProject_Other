# Sediment Analyst
![Inn River](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/river_inn.png "Sample Location")

## Introduction

![Sample Location](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/measuring_points.png "Sample Location")

*Example of location of the collected samples. Ering, Germany*


Sediment Analyst is a modularized Python package-to-be that enables sedimentological analyses. By using sieving datasets as input, Sediment Analyzer computes sediment statistics. The statistics computed are:
- Sediment characteristics (d10, d16, d50, d84, d90, sorting index, mean grain size, etc. ). For more information see the documentation of the class StatisticalAnalyzer.
- Porosity predictors based on available Literature (e.g., Carling & Reader).
- Hydraulic conductivity estimators based on the [Kozeny-Carman Equation](https://cdnsciencepub.com/doi/abs/10.1139/t03-013).

# Requirements

##Libraries

The *Python* libraries used in 

##Input Data

# Package Structure
![Code UML](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/code_uml_sediment_analyst.png "Code UML")

#Code description

##config.py

Module containing all the imported packages and the user inputs necessary for running the StatisticalAnalyzer and StaticPlotter Classes.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`sample_name`| STRING | Name of the sample |
|`header`|  | Number of lines with a header before the dataset|
|`gs_clm`|  | Grain size column index|
|`cw_clm`|  | Class weight column index |
|`porosity`|  | Option to provide the porosity manually |
|`SF_porosity`|  | Statistical parameter which is/are plotted |
|`index_lat`| TUPLE | Sample latitudinal coordinate |
|`index_long`| TUPLE | Sample longitudinal coordinate |
|`folder_path`|  | Path of folder from which the data is read |
|`index_sample_name`|  | Index of the Excel sheet containing the sample name |
|`index_sample_date`|  | Index of the Excel sheet containing the date in which the sample was collected |
|`projection`|  | Definition of the projection |

##utils.py

##statistical_analyzer.py

##static_plotter.py



##main.py

##appconfig.py

##apputils.py

##interac_plotter.py

##web_application.py


