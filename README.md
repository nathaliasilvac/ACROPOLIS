# ACROPOLIS: Classification of risk for off-stream reservoirs using Machine Learning
![Window](Images/Window.png)
ACROPOLIS is a  tool designed for the classification of risk associated with off-stream reservoirs. Utilizing a  Machine Learning algorithm, the tool offers a fast and efficient method for the preliminary estimation of risk classification in these reservoirs [(Silva-Cancino et al., 2022)](https://www.mdpi.com/2073-4441/14/15/2416?utm_campaign=releaseissue_waterutm_medium=emailutm_source=releaseissueutm_term=doilink114). Its incorporation of advanced technology enables users to swiftly assess and categorize risk levels, providing valuable insights for reservoir management and decision-making processes.

## The software tool provides:
1. Visualization of the flow accumulation based on a Digital Elevation Model (DEM)
2. Classification of areas of interest (AoI) as "risk" or "no risk".
3. Overall classification of risk of the off-stream reservoir (A, B or C)
4. Stochastic analysis

## Prerequisites 
We recommend the use of [Anaconda](https://www.anaconda.com/download) to install the dependencies

-[Python 3.8](https://www.python.org/downloads/release/python-380/)

-[pyproj 3.4.1](https://pyproj4.github.io/pyproj/stable/)

-[tkintermapview 1.17](https://github.com/TomSchimansky/TkinterMapView)

-[tkinter 3.17](https://docs.python.org/3/library/tkinter.html)

-[geopandas 0.11](https://geopandas.org/en/stable/)

-[joblib 1.2.0](https://joblib.readthedocs.io/en/latest/installing.html)

-[pillow 9.3.0](https://pillow.readthedocs.io/en/stable/installation.html)

-[pysheds 0.2.7](https://pypi.org/project/pysheds/)

-[rasterio 1.3.4](https://pypi.org/project/rasterio/)   

-[matplotlib 3.6.2](https://matplotlib.org/stable/index.html)

-[numpy 1.23.4](https://numpy.org/install/)

-[pandas 1.5.1](https://pypi.org/project/pandas/)

-[scikit-learn 0.24.1](https://scikit-learn.org/stable/install.html)

 ## Installation  
1. Download all the files from the "Script" folder and save them to your computer.

2. The ML model has been compressed into multiple zip files, which are in the folder ML Model, so to extract it, please download all the zip files in the same folder where the Python script is located and extract the file in ACROPOLIS_ML.zip001.
   
3. Install all the prerequisites making sure to install the correct version. They can be installed using pip or conda.

4. Execute the Python file from the Python console.

## License
ACROPOLIS is distributed under the GNU Affero General Public License v3.0 (AGPL-3.0). This license is specifically designed to guarantee that users interacting with the software over a network, like through a web application, have access to its source code as well. It provides you with the freedom to utilize, modify, and distribute ACROPOLIS in accordance with the terms and conditions stated in the AGPL-3.0 license.

## Disclaimer
CROPOLIS is provided "as-is" and without any warranty. The developers do not offer any assurances regarding the accuracy, reliability, or suitability of the software for any specific purpose.

Under no circumstances shall the developers of ACROPOLIS be liable for any direct, indirect, incidental, special, exemplary, or consequential damages, including but not limited to loss of data, profits, or business interruption, arising from the use or inability to use the ACROPOLIS software.

The user bears full responsibility for the use of materials or information obtained from this application. Any service, repair, or correction of equipment or data required as a result of using ACROPOLIS is solely the responsibility of the user.

## Support
For support, email me at nsilva@cimne.upc.edu
