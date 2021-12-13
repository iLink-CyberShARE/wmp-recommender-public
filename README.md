# SWIM Recommender System 2.0
The SWIM Recommender System is a Restful API implementation that builds upon the python recommendation library LightFM. This application provides a small footprint cyberinfrastructure for storing training data, tracking, and training recommender models with unique approaches on data pre-processing for LightFM consumption.

## Running on Docker
The SWIM Recommender is ready to use as a set of two containers with execution via Docker Composer.   

To try it out:  
1) Download this repository into a folder on your machine    
2) Install Docker and Docker composer on your target machine    
3) Setup your docker account at: https://www.docker.com/get-started    
4) Using a command line or terminal navigate to the base path of the project  
5) Build the swim-recomm image: > docker build -t swim-recomm:latest .    
6) Modify the file docker-compose.yml accordingly  
6) Run docker compose: > docker-compose up  
7) Once running, the API docs will be locally available at http://localhost:5000/swim-recommender/docs/  (default connection on docker compose file)  

## Native Installation

### General Dependencies:  
+ Python > 3
+ pip packages from requirements.txt recommended to install on python virtual env.
   >> pip install -r requirements.txt

### Windows Dependencies:
C++ build tools from visual studio "cl.exe" required to install lightfm 
Microsoft Visual C++ Build Tools
+ https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16

### Linux Dependencies (CentOS 7):
+ sudo yum install mysql-devel gcc python-devel   => mysql drivers

### Virtual Environment:   
Follow the Python DOCS to create a virtual environment in python and install dependency packages from requirements.txt
+ Note: update pip after creating and activating the virtual environment, otherwise some package dependency errors might come up.
+ Python DOCS: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

### CLI Run Commands:  
+ localhost run server (development mode): > py manage.py run (windows)
+ run optimization trials (modify code to your data): > py manage.py optimize

### Production Server:
+ Tested on CentOS 7 & CentOS 8
+ Install uWSGI
+ Run uWSGI with app.ini settings.

## Data   
1. A sql dump of optuna trial runs is available under database/backups.
2. A summary of optimized results is available under model/study-results 08252021 1449.txt  
3. Coming Soon - Sample data from SWIM UI

## Default user sample accounts
JWT generation endpoint: <host>:<port>/auth

JSON payload:
{
   "username" : "<email>",
   "password" : "<password>"
}

For content manager (high authorization level) use the following default credentials to generate JWT token:
username: manager@email.com
password: precommanger2021

For normal user (low authorization level) use the following default
credentials to generate JWT token:
username: uiaccess@email.com
password: urecommui2021

## Acknowledgements
This material is based upon work supported by the National Science
Foundation (NSF) under Grant No. 1835897. This work used resources from
Cyber-ShARE Center of Excellence, which is supported by NSF Grant number
HRD-1242122.      
Any opinions, findings, and conclusions or recommendations
expressed in this material are those of the author(s) and do not necessarily
reflect the views of the NSF. 

Maciej Kula - Author of LightFM library code base.

## Contributors
Project PI - Natalia Villanueva-Rosales  
Project Co-PI - Deana D. Pennington  
Project Co-PI - Josiah Heyman  
Lead Developer - Luis A. Garnica Chavira  
Developer - Aaron Zambrano  
Developer - Manuel Henandez  

## License
GNU GENERAL PUBLIC LICENSE v3.0

## Copyright
© 2021 - University of Texas at El Paso (Luis A. Garnica Chavira). 

## References: 
+ SQLALCHEMY: Database ORM for python: https://www.sqlalchemy.org/
+ Flask: Webservice API wrapping: https://www.fullstackpython.com/flask.html
+ CORS: To call the API from outside the localhost domain: https://flask-cors.readthedocs.io/en/latest/
+ LightFM: https://lyst.github.io/lightfm/docs/home.html
    - Quickstart: https://github.com/lyst/lightfm/blob/master/examples/quickstart/quickstart.ipynb

