# WMP Recommender System 2.0
The WMP Recommender System is a Restful API implementation that builds upon the python recommendation library LightFM. This application provides a small footprint cyberinfrastructure for storing training data, tracking, and training recommender models with unique approaches on data pre-processing for LightFM consumption.

## Running on Docker
The WMP-RS is ready to use as a set of two containers with execution via Docker Composer.

To try it out:  
1) Download this repository into a folder on your machine    
2) Install Docker and Docker composer on your target machine    
3) Setup your docker account at: https://www.docker.com/get-started    
4) Using a command line or terminal navigate to the base path of the project  
5) Build the swim-recomm image: > docker build -t swim-recomm:latest .    
6) Modify the file docker-compose.yml accordingly  
6) Run the containers: > docker-compose up  
7) Once running, the API docs will be locally available at http://localhost:5000/swim-recommender/docs/

### Demo Video
Click on the following link to watch an API demo using Docker and Swagger Documentation:   
https://emalm.com/?v=QYAAG

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
+ localhost (development mode): > py manage.py run (windows)
+ localhost (run optimization trials): > py manage.py optimize
+ external access (test) > python3 manage.py  runserver --host 129.108.18.45 --port 5000 (linux)   

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

## Acknowledgements
 

## Authors


## Credits
Use with no modifications of:   
LightFM © Copyright 2016, Lyst (Maciej Kula) - Apache License v2.0   
https://www.apache.org/licenses/LICENSE-2.0.html

Use of:   
SQLAlchemy, a trademark of Michael Bayer. mike(&)zzzcomputing.com All rights reserved. - MIT License   
https://mit-license.org/   

Use of:
Flask, Copyright 2010 Pallets. - BSD 3-Clause "New" or "Revised" License
https://github.com/pallets/flask/blob/main/LICENSE.rst

## License
GNU GENERAL PUBLIC LICENSE v3.0

## Copyright
© 2019 - 2021, The University of Texas at El Paso (SWIM Project)

## References: 
+ SQLALCHEMY: Database ORM for python: https://www.sqlalchemy.org/
+ Flask: Webservice API wrapping: https://www.fullstackpython.com/flask.html
+ CORS: To call the API from outside the localhost domain: https://flask-cors.readthedocs.io/en/latest/
+ LightFM: https://lyst.github.io/lightfm/docs/home.html
    - Quickstart: https://github.com/lyst/lightfm/blob/master/examples/quickstart/quickstart.ipynb

