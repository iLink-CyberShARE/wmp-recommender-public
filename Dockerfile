# Pull centos 8 image
# TODO: use lighter base such as alpine
FROM centos:8.3.2011

# Update the environment and perform yum installations
RUN yum update -y \
    && yum install -y python3 \
    && yum install -y mysql-devel gcc python3-devel \
    && yum install -y jq \
    && yum clean all

# create a directory for bash files
WORKDIR /cronjobs

# copy bash scripts
COPY  /bash /cronjobs

# TODO: setup a cronjob here for periodic model re-training

# Set the working directory to /recommender
WORKDIR /recommender

# Copy project directory into the container at /recommender
COPY  . /recommender

# Update pip and setup virtual python environment
RUN python3 -m pip --no-cache-dir install --user --upgrade pip \
    && python3 -m pip --no-cache-dir install --user virtualenv \
    && python3 -m venv env \
    && source env/bin/activate

# Install the dependencies
RUN python3 -m pip --no-cache-dir install -r requirements.txt

# Expose port
EXPOSE 5000

# Production WSGI Server
CMD ["uwsgi", "app.ini"]