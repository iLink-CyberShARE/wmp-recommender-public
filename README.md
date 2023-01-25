# SWIM Recommender System 2.0
The SWIM Recommender System is a Restful API implementation that builds upon the python recommendation library LightFM. This application provides a small footprint cyberinfrastructure for storing training data, tracking, and training recommender models with unique approaches on data pre-processing for LightFM consumption.

## Build and Run

### Recommender execution environment
+ Python > 3
+ pip packages from requirements.txt recommended to install on python virtual env.

### Option 1: Docker Compose File
1. Download the docker-composer.yml file to a path in your machine.   
2. Install Docker and Docker composer on your target machine.   
3. Setup your docker account at: https://www.docker.com/get-started   
4. Configure the docker-composer file with your own app settings.   
5. Run docker compose: $docker-compose up   
5a. Use -d option on the composer command to run on the background.   
6. Swagger docs available at http://localhost:5000/swim-recommender/docs/ 

### Option 2: Build Docker Container
1) Download this repository into a folder on your machine    
2) Install Docker and Docker composer on your target machine    
3) Setup your docker account at: https://www.docker.com/get-started    
4) Using a command line or terminal navigate to the base path of the project  
5) Build the swim-recomm image: > docker build -t swim-recomm:latest .    
6) Modify the file docker-compose.yml accordingly  
6) Run docker compose: > docker-compose up  
7) Once running, the API docs will be locally available at http://localhost:5000/swim-recommender/docs/  (default connection on docker compose file)  

### Option 3: Native

*Windows Dependencies:*   
C++ build tools from visual studio "cl.exe" required to install lightfm 
Microsoft Visual C++ Build Tools
+ https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16

*Linux Dependencies (CentOS 7):*   
+ sudo yum install mysql-devel gcc python-devel   => mysql drivers

1. Follow the Python DOCS to create a virtual environment in python and install dependency packages from requirements.txt
+ Note: update pip after creating and activating the virtual environment, otherwise some package dependency errors might come up.
+ Python DOCS: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

2. CLI Run Commands:  
+ localhost run server (development mode): > py manage.py run (windows)
+ run optimization trials (modify code to your data): > py manage.py optimize

3. Production Server:
+ Tested on CentOS 7 & CentOS 8
+ Install uWSGI
+ Run uWSGI with app.ini settings.

## Data   
1. A sql dump of optuna trial runs is available under database/backups.
2. A summary of optimized results is available under model/study-results 08252021 1449.txt  

## User Account Setup

*Default user sample accounts*   
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

## Documentation
[SWIM Recommender](https://water.cybershare.utep.edu/resources/docs/en2/backend/recommender-api/)

## Screenshots
**List of available endpoints**  
![Alt text](screenshots/endpoint_list.jpg?raw=true "Endpoint Listing")

**Training Endpoint**   
![Alt text](screenshots/training_endpoint.jpg?raw=true "Training Endpoint")

**Evaluation Response**   
![Alt text](screenshots/evaluation_response.jpg?raw=true "Evaluation Response")

**Recommendation Response**   
![Alt text](screenshots/recommendation_response.jpg?raw=true "Recommendation Response")

## Acknowledgements
This material is based upon work supported by the National Science Foundation (NSF) under Grant No. 1835897.   

Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.  

Maciej Kula - Original author of LightFM library code base.

## Contributors
Luis A. Garnica Chavira  
Aaron Zambrano     
Josiah Heyman     
Manuel Henandez     

## License
This software code is licensed under the [GNU GENERAL PUBLIC LICENSE v3.0](./LICENSE) and uses third party libraries that are distributed under their own terms (see [LICENSE-3RD-PARTY.md](./LICENSE-3RD-PARTY.md)).

## Copyright
© 2019-2023 - University of Texas at El Paso (SWIM Project).


