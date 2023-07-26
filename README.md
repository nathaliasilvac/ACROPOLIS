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
Please download all the files from the "Script" folder and save them to your computer in the same folder. The ML model has been compressed into multiple zip files, which are in the folder ML Model, so to extract it, please download all the zip files in the same folder where the python script is located and extract the file in ACROPOLIS_ML.zip001.

Execute the Python file from the Python console or any other console, such as Spyder.

## Support
For support, email me at nsilva@cimne.upc.edu
