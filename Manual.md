# ACROPOLIS: User Manual
To use the application, the user must perform a pre-processing step, which involves estimating the input data for the model, collecting terrain details, and locating the areas of concern to evaluate.
This manual provides a step-by-step guide for the user, from data pre-processing to estimating the reservoir classification.
# 1. Pre-process:
The pre-processing is divided into four parts: 1) Downloading the digital elevation model (DEM), 2) Assigning roughness, 3) Locating affected areas, and 4) Estimating physical parameters.

## 1.1 Digital Elevation Model (DEM):
There are various portals and tools available for downloading digital elevation models. In Spain,  the [Download Center of the National Geographic Institute (IGN)](https://centrodedescargas.cnig.es/CentroDescargas/index.jsp), offers free access to geographic information. By providing the reservoir's coordinates, users can search for and download the corresponding DEM.
![dem](Images/dem.bmp) 
Typically, the downloaded files are in ASCII format. The tool can directly read these files or, if preferred, users can opt for the TIF format. It is advisable for users to review the downloaded file using GIS software, such as [QGIS](https://www.qgis.org/en/site/forusers/download.html). This allows them to crop the DEM if desired. Note that processing time may increase for larger DEMs.







