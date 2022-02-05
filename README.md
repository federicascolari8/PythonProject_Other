# Sediment Analyst
## Introduction
Sediment Analyst is a modularized Python package-to-be that enables sedimentological analyses. By using sieving datasets as input, Sediment Analyzer computes sediment statistics. The statistics computed are:
- Sediment characteristics (d10, d16, d50, d84, d90, sorting index, mean grain size, etc. ). For more information see the documentation of the class StatisticalAnalyzer.
- Porosity predictors based on available Literature (e.g., Carling & Reader).
- Hydraulic conductivity estimators based on the [Kozeny-Carman Equation](https://cdnsciencepub.com/doi/abs/10.1139/t03-013).

# Package Structure
![Code UML](/assets/code_uml_sediment_analyst.png "Code UML")
