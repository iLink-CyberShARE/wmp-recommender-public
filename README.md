# WMP Recommender System 2.0
The WMP Recommender System is a Restful API implementation that builds upon the python recommendation library LightFM. This application provides a small footprint cyberinfrastructure for storing training data, tracking, and training recommender models with unique approaches on data pre-processing for LightFM consumption.

## Docker Containers
The WMP-RS is ready to use as a set of two containers with execution via Docker Composer.

To try it out:
1) Download this repository into a folder on your machine.
2) Install Docker and Docker composer on your target machine.
3) Setup your docker account at: https://www.docker.com/get-started
4) Using a command line or terminal navigate to the base path of the project.
5) Build the swim-recomm image: > docker build -t swim-recomm:latest .
6) Modify the file docker-compose.yml accordingly.
6) Run the containers: > docker-compose up
7) Once running, the API docs will be locally available at http://localhost:5000/swim-recommender/docs/ where you can test out the service endpoints with the pre-populated sample database (default connection on docker compose file)

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

### Run Commands:  
+ localhost (debug): > py manage.py run (windows)
+ external access (test) >python3 manage.py  runserver --host 129.108.18.45 --port 5000 (linux)   

### Production Server:
+ Tested on CentOS 7 & CentOS 8
+ Install uWSGI
+ Run uWSGI with app.ini settings.

## Default user sample accounts
JWT generation endpoint: <host>:<port>/auth

JSON payload:
{
   "username" : "<email>"
   "password" : "<password>"
}

For content manager (high authorization level) use the following default credentials to generate JWT token:
username: manager@email.com
password: precommanger2021

For normal user (low authorization level) use the following default
credentials to generate JWT token:
username: uiaccess@email.com
password: urecommui2021

## Solved Issues:
+ cannot import name 'cached_property' from 'werkzeug' 
   - Fix: pip install Werkzeug==0.16.1
+ swagger url source paths are not relative
   - Fix: extended as custom api on flask-restplus to set: return url_for(self.endpoint('specs'), _external=False) on def specs_url(self):
+ MYSQL server has gone away after connection is idle and killed by mysql server (default 8 hours)
   - Fix: start and close session on all services called by endpoints
   - Hotfix: setup a cronjob to restart service before mysql session expiration.
   - More info: https://topic.alibabacloud.com/a/mysql-has-gone-away-several-possible_1_41_30014708.html

## Acknowledgements
This material is based upon work supported by NSF Grant No. 1835897   

Maciej Kula - Author of LightFM library code base.

## Authors
Project PI - Natalia Villanueva-Rosales  
Project Co-PI - Deana D. Pennington  
Project Co-PI - Josiah Heyman  
Lead Developer - Luis A. Garnica Chavira  
Developer - Aaron Zambrano  
Developer - Manuel Henandez  

## License
GNU GENERAL PUBLIC LICENSE

## References: 
+ SQLALCHEMY: Database ORM for python: https://www.sqlalchemy.org/
+ Flask: Webservice API wrapping: https://www.fullstackpython.com/flask.html
+ CORS: To call the API from outside the localhost domain: https://flask-cors.readthedocs.io/en/latest/
+ LightFM: https://lyst.github.io/lightfm/docs/home.html
    - Quickstart: https://github.com/lyst/lightfm/blob/master/examples/quickstart/quickstart.ipynb

