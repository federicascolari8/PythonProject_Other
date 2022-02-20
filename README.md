# Sediment Analyst
![Inn River](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/river_inn.png "Sample Location")

## Welcome

Sediment Analyst is a modularized Python package that enables sedimentological analyses. 

![Sample Location](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/measuring_points.png "Sample Location")

*Example of location of the collected samples. Ering, Germany*


By using sieving datasets as input, Sediment Analyzer computes sediment statistics. The statistics computed are:
- Sediment characteristics (d10, d16, d50, d84, d90, sorting index, mean grain size, etc. ). For more information see the documentation of the class StatisticalAnalyzer.
- Porosity predictors based on available Literature (e.g., Carling & Reader).
- Hydraulic conductivity estimators based on the [Kozeny-Carman Equation](https://cdnsciencepub.com/doi/abs/10.1139/t03-013).

# Requirements

##Libraries

The used *Python* libraries are: *numpy*, *scipy*, *pathlib*, *matplotlib*, *openpyxl*, *pandas*, *seaborn*, *dash*, *pyproj*, *plotly.express*.

Standard libraries: *re*, *locale*, *logging*, *glob*, *sys*, *os*, *math*

Checkout the requirements.txt file for seeing the version requirements of the packages.

##Input Data

The input data consists of excel/csv files for each sediment sample. For correctly parsing the datasets checkout the tutorial below.


# Package Structure
![Code UML](https://github.com/federicascolari8/PythonProject_Other/raw/main/assets/code_uml_sediment_analyst.png "Code UML")

# Link to app

[![Applink]([![Foo](https://raw.githubusercontent.com/federicascolari8/PythonProject_Other/main/assets/intro_w_image.jpg)](http://google.com.au/))](https://sedimentanalyst.herokuapp.com/)

Checkout the [video tutorial](https://youtu.be/zXfN9-M12i0)

#Code description

##config.py

Module containing all the imported packages and the user inputs necessary for running the StatisticalAnalyzer and StaticPlotter Classes.

| Input | Type | Description |
|-----------------|------|-------------|
|`sample_name`| STR | Name of the sample |
|`header`| INT | Number of lines with a header before the dataset|
|`gs_clm`| INT | Grain size column index|
|`cw_clm`| INT | Class weight column index |
|`porosity`| LIST | Option to provide the porosity manually |
|`SF_porosity`| LIST | Statistical parameter which is/are plotted |
|`index_lat`| LIST | Sample latitudinal coordinate |
|`index_long`| LIST | Sample longitudinal coordinate |
|`folder_path`| STR | Path of folder from which the data is read |
|`index_sample_name`| LIST | Index of the Excel sheet containing the sample name |
|`index_sample_date`| LIST | Index of the Excel sheet containing the date in which the sample was collected |
|`projection`| STR | Definition of the projection |

##utils.py

##statistical_analyzer.py

<br/>

##static_plotter.py

File in which the `StaticPlotter` Class is stored. This Class defines the methods which allow the
plotting and saving as an image of the cumulative grain size distribution curve for each collected sample.

The methods composing the `StaticPlotter` Class are the following:

### `__init__()`

Initializes a StatisticalAnalyzer variable and a dataframe by using the analyzer object.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`analyzer`| StatisticalAnalyzer  | Internally used StatisticalAnalyzer object. |


### `cum_plotter()`
Plots the cumulative grain size distribution curve and saves it as an image.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`output`| STR  | Name of the saved image containing the plot. |

**return:** None

### `__set_main_sec_axis()`

Private method used to set the main secondary axis with the axis *ax* as input argument.

**return:** None

### `__set_min_sec_axis()`

Private method used to set the minor secondary axis with the axis *ax2* as input argument.

**return:** None

### `__set_axis_colour_and_format()`

Private method with the axis *ax* as input, used to define the following:
- Axis tick values for the x-axis.
- Axis tick values for the y-axis. 
- Vertical line across the axis properties.
- Axes labels.

**return:** None

<br/>

##main.py

File where the DataFrame is instantiated, the user-input in retrieved and a list of the files in the user selected folder is created.
Samples contained in the files are then computed.

<br/>

##appconfig.py

Module containing the imported packages necessary to correctly configure the environment for *web_application.py* and *interac_plotter.py*

<br/>

##apputils.py


<br/>

##interac_plotter.py
Module containing the `InteractivePlotter` Class. It has been designed for the creation of the map, 
used to indicate the location of the collected samples, and the interactive plots necessary for the 
comparison of the results of the statistical analysis.  
Here below the description of the methods defined in the `InteractivePlotter` Class:

### `convert_coordinates()`

Transforms the coordinates of a give projection in degrees.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`df`| ?  | Dataframe on which the coordinate transformation is applied. |
|`projection`| STR  | Name of the initial projection. |

**return:** df (TYPE MISSING)

### `create_map()`
Creates a scatter map based on the data contained in the dataframe.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`df`| ?  | Dataframe on which the coordinate transformation is applied. |
|`projection`| STR  | Name of the initial projection. |
|`samples`| LIST  | Names of the samples. |

**return:** fig (TYPE MISSING)

### `plot_histogram()`

Plots the results in a bar chart based on the statistical parameters selected by the user.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`param`| STR  | Parameters among which the user can choose for the results visualization. |
|`samples`| LIST  | Names of the samples. |

**return:** fig (TYPE MISSING)

### `plot_gsd()`

Plots the cumulative grain size distribution curve for all selected samples.

| Input argument | Type | Description |
|-----------------|------|-------------|
|`samples`| LIST  | Names of the samples. |

**return:** fig (TYPE MISSING)

<br/>

##web_application.py


