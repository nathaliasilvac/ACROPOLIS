# ACROPOLIS: Classification of risk for off-stream reservoirs using Machine Learning
![Window](Images/Window.png)
ACROPOLIS is a  tool designed for the classification of risk associated with off-stream reservoirs. Utilizing a  Machine Learning algorithm, the tool offers a fast and efficient method for the preliminary estimation of risk classification in these reservoirs [(Silva-Cancino et al., 2022)](https://www.mdpi.com/2073-4441/14/15/2416?utm_campaign=releaseissue_waterutm_medium=emailutm_source=releaseissueutm_term=doilink114). Its incorporation of advanced technology enables users to swiftly assess and categorize risk levels, providing valuable insights for reservoir management and decision-making processes.

## The software tool provides:
1. Visualization of the flow accumulation based on a Digital Elevation Model (DEM)
2. Classification of areas of interest (AoI) as "risk" or "no risk".
3. Overall classification of risk of the off-stream reservoir (A, B or C)
4. Stochastic analysis

## Prerequisites
We recommend the use of [Anaconda](https://www.anaconda.com/download) to run and create environments.
The prerequisites for using ACROPOLIS are as follows:
-[Python >=3.8](https://www.python.org/downloads/release/python-3817/)

-geopandas, joblib, matplotlib, numpy, panda, patool, pillow, pyproj, pysheds, rasterio, scikit-learn and shutils.

The recommended versions of the packages are found in requirements.txt

 ## Installation

1. **Clone the Repository:**
   ```
   git clone https://github.com/your-username/ACROPOLIS.git
   ```

2. **Create a new conda environment in the Anaconda prompt and activate**
   ```
   conda create --name ACROPOLIS
   ```
   ```
   conda activate ACROPOLIS
   ```
   
3. **Install the packages listed in the requirements.txt file**
   ```
    pip install -r requirements.txt
   ```
   
4. **Execute the Python file (ACROPOLIS.py)**
   ```
    Python ACROPOLIS.py
   ```
## License
ACROPOLIS is distributed under the GNU Affero General Public License v3.0 (AGPL-3.0). This license is specifically designed to guarantee that users interacting with the software over a network, like through a web application, have access to its source code as well. It provides you with the freedom to utilize, modify, and distribute ACROPOLIS in accordance with the terms and conditions stated in the AGPL-3.0 license.

---

**Disclaimer:**
ACROPOLIS is provided "as-is" and without any warranty. The developers do not offer any assurances regarding the accuracy, reliability, or suitability of the software for any specific purpose.

Under no circumstances shall the developers of ACROPOLIS be liable for any direct, indirect, incidental, special, exemplary, or consequential damages, including but not limited to loss of data, profits, or business interruption, arising from the use or inability to use the ACROPOLIS software.

The user bears full responsibility for the use of materials or information obtained from this application. Any service, repair, or correction of equipment or data required as a result of using ACROPOLIS is solely the responsibility of the user.

## Support
For support, email me at nsilva@cimne.upc.edu
