############################################################
# Dockerfile to run a Django-based web application
# Based on an Ubuntu Image
############################################################

# Set the base image to use to Ubuntu
FROM ubuntu:14.04

# Set the file maintainer
MAINTAINER Anson Bastos

# Set env variables used in this Dockerfile (add a unique prefix, such as DOCKYARD)
# Local directory with project source
ENV DOCKYARD_SRC=Project
# Directory in container for all project files
ENV DOCKYARD_SRVHOME=/srv
# Directory in container for project source files
ENV DOCKYARD_SRVPROJ=/srv/Project

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip

WORKDIR $DOCKYARD_SRVHOME

# Copy application source code to SRCDIR
COPY $DOCKYARD_SRC $DOCKYARD_SRVPROJ

RUN sudo apt-get install -y apt-transport-https

#Install Mongodb
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
RUN sudo apt-get update
RUN sudo apt-get install -y mongodb-org

# Install Python dependencies
RUN pip3 install -r $DOCKYARD_SRVPROJ/requirements.txt

# Port to expose
EXPOSE 8000

# Copy entrypoint script into the image
WORKDIR $DOCKYARD_SRVPROJ
COPY ./docker-entrypoint.sh /

RUN mkdir /data
RUN mkdir /data/db

ENTRYPOINT ["/docker-entrypoint.sh"]